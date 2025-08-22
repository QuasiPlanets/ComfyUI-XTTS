import os
import time
import torch
import torchaudio
import folder_paths
import cuda_malloc
from srt import parse as SrtPare
from pydub import AudioSegment
import audiotsm
import audiotsm.io.wav
from huggingface_hub import snapshot_download
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'TTS'))
from tts.models.xtts import Xtts
from tts.configs.xtts_config import XttsConfig

now_dir = os.path.dirname(os.path.abspath(__file__))
input_path = folder_paths.get_input_directory()
output_path = folder_paths.get_output_directory()
pretrained_models_path = os.path.join(now_dir, "pretrained_models")
os.makedirs(pretrained_models_path, exist_ok=True)

language_list = ["en","es","fr","de","it","pt","pl","tr","ru",
                         "nl","cs","ar","zh-cn","ja","hu","ko","hi"]
class XTTS_INFER_SRT:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                     "text": ("SRT",),
                     "prompt_audio": ("AUDIOPATH",),
                     "language": (language_list,{
                         "default": "zh-cn"
                     }),
                    "if_mutiple_speaker":("BOOLEAN",{
                        "default": False
                    }),
                     "temperature":("FLOAT",{
                         "default":0.7,
                         "min":0,
                         "max": 1,
                         "step": 0.05,
                         "display": "slider"
                     }),
                     "length_penalty":("FLOAT",{
                         "default":1.0
                     }),
                     "repetition_penalty":("FLOAT",{
                         "default":4.0
                     }),
                     "top_k":("INT",{
                         "default":50,
                     }),
                     "top_p":("FLOAT",{
                         "default":0.85,
                         "min":0,
                         "max": 1,
                         "step": 0.05,
                         "display": "slider"
                     }),
                     "speed":("FLOAT",{
                         "default":1.0,
                     }),
                     }
                }

    CATEGORY = "AIFSH_XTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("AUDIOPATH",)

    OUTPUT_NODE = False

    FUNCTION = "get_wav_tts"

    def get_wav_tts(self,text,prompt_audio,language,if_mutiple_speaker,
                    temperature,length_penalty,
                    repetition_penalty,top_k,top_p,speed):
        xtts_tmp_path = os.path.join(output_path, 'xtts')
        os.makedirs(xtts_tmp_path, exist_ok=True)
        if not os.path.isfile(os.path.join(pretrained_models_path,"model.pth")):
            print("Downloading model...")
            snapshot_download(repo_id="coqui/XTTS-v2",revision="v2.0.3",local_dir=pretrained_models_path)
        print("Loading model...")
        config = XttsConfig()
        config.load_json(os.path.join(pretrained_models_path, "config.json"))
        model = Xtts.init_from_config(config)
        model.load_checkpoint(config, checkpoint_dir=pretrained_models_path, use_deepspeed=False)
        if cuda_malloc.cuda_malloc_supported():
            model.cuda()
        
        with open(text, 'r', encoding="utf-8") as file:
            text_file_content = file.read()
        text_subtitles = list(SrtPare(text_file_content))
        spk_aduio_dict = {}
        audio_seg = AudioSegment.from_file(prompt_audio)
        gpt_embedding_dict = {}
        if if_mutiple_speaker:
            for i,text_sub in enumerate(text_subtitles):
                start_time = text_sub.start.total_seconds() * 1000
                end_time = text_sub.end.total_seconds() * 1000
                speaker = 'SPK'+text_sub.content[0]
                try:
                    spk_aduio_dict[speaker] += audio_seg[start_time:end_time]
                except:
                    spk_aduio_dict[speaker] = audio_seg[start_time:end_time]
            for speaker in spk_aduio_dict.keys():
                speaker_audio_seg = spk_aduio_dict[speaker]
                speaker_audio = os.path.join(xtts_tmp_path, f"{speaker}.wav")
                speaker_audio_seg.export(speaker_audio,format='wav')
                gpt_embedding_dict[speaker] = model.get_conditioning_latents(audio_path=[speaker_audio])
        else:
            print(f"Computing speaker SPK0 latents...")
            gpt_embedding_dict["SPK0"] = model.get_conditioning_latents(audio_path=[prompt_audio])
        
        new_audio_seg = AudioSegment.silent(0)
        for i,text_sub in enumerate(text_subtitles):
            start_time = text_sub.start.total_seconds() * 1000
            end_time = text_sub.end.total_seconds() * 1000
            if i == 0:
                new_audio_seg += audio_seg[:start_time]
                
            new_text = text_sub.content
            if if_mutiple_speaker:
                speaker = "SPK" + new_text[0]
                new_text = new_text[1:]
            else:
                speaker = "SPK0"
            gpt_cond_latent,speaker_embedding = gpt_embedding_dict[speaker]
            print(f"use {speaker} voice Inference: {new_text}")
            
            # Intelligent text chunking for SRT processing
            max_chars_per_chunk = 250  # Conservative limit for XTTS-v1
            if len(new_text) > max_chars_per_chunk:
                print(f"SRT text length ({len(new_text)} chars) exceeds chunk limit, processing in chunks...")
                # Split into sentences or natural breaks
                sentences = new_text.replace('!', '.').replace('?', '.').split('.')
                chunks = []
                current_chunk = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                        
                    # If adding this sentence would exceed limit, start new chunk
                    if len(current_chunk + sentence) > max_chars_per_chunk and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        current_chunk += sentence + ". "
                
                # Add the last chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                print(f"Split SRT text into {len(chunks)} chunks for processing")
                
                # Process each chunk and concatenate audio
                all_audio = []
                for j, chunk in enumerate(chunks):
                    print(f"Processing SRT chunk {j+1}/{len(chunks)}: {chunk[:50]}...")
                    chunk_out = model.inference(
                        chunk,
                        language,
                        gpt_cond_latent,
                        speaker_embedding,
                        temperature=temperature,
                        length_penalty=length_penalty,
                        repetition_penalty=repetition_penalty,
                        top_k=top_k,
                        top_p=top_p,
                        speed=speed,
                        enable_text_splitting=False  # Disable internal splitting since we're doing it manually
                    )
                    all_audio.append(chunk_out["wav"])
                
                # Concatenate all audio chunks
                import numpy as np
                concatenated_audio = np.concatenate(all_audio)
                out = {"wav": concatenated_audio}
            else:
                # Single chunk processing
                out = model.inference(
                    new_text,
                    language,
                    gpt_cond_latent,
                    speaker_embedding,
                    temperature=temperature,
                    length_penalty=length_penalty,
                    repetition_penalty=repetition_penalty,
                    top_k=top_k,
                    top_p=top_p,
                    speed=speed,
                    enable_text_splitting=False  # Disable internal splitting for single chunks
                )
            wav_path = os.path.join(xtts_tmp_path, f"{i}_xtts.wav")
            torchaudio.save(wav_path, torch.tensor(out["wav"]).unsqueeze(0), 24000,bits_per_sample=16)
            
            text_audio = AudioSegment.from_file(wav_path)
            text_audio_dur_time = text_audio.duration_seconds * 1000
            
            if i < len(text_subtitles) - 1:
                nxt_start = text_subtitles[i+1].start.total_seconds() * 1000
                dur_time =  nxt_start - start_time
            else:
                org_dur_time = audio_seg.duration_seconds * 1000
                dur_time = org_dur_time - start_time
            
            ratio = text_audio_dur_time / dur_time

            if text_audio_dur_time > dur_time:
                tmp_audio = self.map_vocal(audio=text_audio,ratio=ratio,dur_time=dur_time,
                                                wav_name=f"map_{i}_refer.wav",temp_folder=xtts_tmp_path)
                tmp_audio += AudioSegment.silent(dur_time - tmp_audio.duration_seconds*1000)
            else:
                tmp_audio = text_audio + AudioSegment.silent(dur_time - text_audio_dur_time)
          
            new_audio_seg += tmp_audio

        infer_audio = os.path.join(output_path, f"{time.time()}_xtts_refer.wav")
        new_audio_seg.export(infer_audio, format="wav")
            
        del model;import gc;gc.collect();torch.cuda.empty_cache()
        return (infer_audio,)
    
    def map_vocal(self,audio:AudioSegment,ratio:float,dur_time:float,wav_name:str,temp_folder:str):
        tmp_path = f"{temp_folder}/map_{wav_name}"
        audio.export(tmp_path, format="wav")
        
        clone_path = f"{temp_folder}/cloned_{wav_name}"
        reader = audiotsm.io.wav.WavReader(tmp_path)
        
        writer = audiotsm.io.wav.WavWriter(clone_path,channels=reader.channels,
                                        samplerate=reader.samplerate)
        wsloa = audiotsm.wsola(channels=reader.channels,speed=ratio)
        wsloa.run(reader=reader,writer=writer)
        audio_extended = AudioSegment.from_file(clone_path)
        return audio_extended[:dur_time]


class XTTS_INFER:
        
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"audio": ("AUDIOPATH",),
                     "text": ("STRING",{
                         "default": "你好啊！世界",
                         "multiline": True
                      }),
                     "language": (language_list,{
                         "default": "zh-cn"
                     }),
                     "temperature":("FLOAT",{
                         "default":0.7,
                         "min":0,
                         "max": 1,
                         "step": 0.05,
                         "display": "slider"
                     }),
                     "length_penalty":("FLOAT",{
                         "default":1.0
                     }),
                     "repetition_penalty":("FLOAT",{
                         "default":4.0
                     }),
                     "top_k":("INT",{
                         "default":50,
                     }),
                     "top_p":("FLOAT",{
                         "default":0.85,
                         "min":0,
                         "max": 1,
                         "step": 0.05,
                         "display": "slider"
                     }),
                     "speed":("FLOAT",{
                         "default":1.0,
                     }),
                     }
                }

    CATEGORY = "AIFSH_XTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("AUDIOPATH",)

    OUTPUT_NODE = False

    FUNCTION = "get_wav_tts"

    def get_wav_tts(self, audio, text,language,temperature,length_penalty,
                    repetition_penalty,top_k,top_p,speed):
        if not os.path.isfile(os.path.join(pretrained_models_path,"model.pth")):
            print("Downloading model...")
            snapshot_download(repo_id="coqui/XTTS-v2",revision="v2.0.3",local_dir=pretrained_models_path)
        print("Loading model...")
        config = XttsConfig()
        config.load_json(os.path.join(pretrained_models_path, "config.json"))
        model = Xtts.init_from_config(config)
        model.load_checkpoint(config, checkpoint_dir=pretrained_models_path, use_deepspeed=False)
        if cuda_malloc.cuda_malloc_supported():
            model.cuda()
        
        print("Computing speaker latents...")
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[audio])

        print("Inference...")
        
        # Intelligent text chunking for long text (based on operational XTTS patterns)
        # XTTS-v1 can handle ~250-300 characters per chunk safely
        max_chars_per_chunk = 250  # Conservative limit for XTTS-v1
        if len(text) > max_chars_per_chunk:
            print(f"Text length ({len(text)} chars) exceeds chunk limit, processing in chunks...")
            # Split into sentences or natural breaks
            sentences = text.replace('!', '.').replace('?', '.').split('.')
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                    
                # If adding this sentence would exceed limit, start new chunk
                if len(current_chunk + sentence) > max_chars_per_chunk and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += sentence + ". "
            
            # Add the last chunk
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            print(f"Split into {len(chunks)} chunks for processing")
            
            # Process each chunk and concatenate audio
            all_audio = []
            for i, chunk in enumerate(chunks):
                print(f"Processing chunk {i+1}/{len(chunks)}: {chunk[:50]}...")
                chunk_out = model.inference(
                    chunk,
                    language,
                    gpt_cond_latent,
                    speaker_embedding,
                    temperature=temperature,
                    length_penalty=length_penalty,
                    repetition_penalty=repetition_penalty,
                    top_k=top_k,
                    top_p=top_p,
                    speed=speed,
                    enable_text_splitting=False  # Disable internal splitting since we're doing it manually
                )
                all_audio.append(chunk_out["wav"])
            
            # Concatenate all audio chunks
            import numpy as np
            concatenated_audio = np.concatenate(all_audio)
            out = {"wav": concatenated_audio}
        else:
            # Single chunk processing
            out = model.inference(
                text,
                language,
                gpt_cond_latent,
                speaker_embedding,
                temperature=temperature,
                length_penalty=length_penalty,
                repetition_penalty=repetition_penalty,
                top_k=top_k,
                top_p=top_p,
                speed=speed,
                enable_text_splitting=False  # Disable internal splitting for single chunks
            )
        wav_path = os.path.join(output_path, f"{time.time()}_xtts.wav")
        torchaudio.save(wav_path, torch.tensor(out["wav"]).unsqueeze(0), 24000,bits_per_sample=16)
        del model;import gc;gc.collect();torch.cuda.empty_cache()
        return (wav_path,)

class PreViewAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"audio": ("AUDIOPATH",),}
                }

    CATEGORY = "AIFSH_XTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_name = os.path.basename(audio)
        tmp_path = os.path.dirname(audio)
        audio_root = os.path.basename(tmp_path)
        return {"ui": {"audio":[audio_name,audio_root]}}

class LoadAudioPath:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1].lower() in ["wav", "mp3","flac","m4a"]]
        return {"required":
                    {"audio": (sorted(files),)},
                }

    CATEGORY = "AIFSH_XTTS"

    RETURN_TYPES = ("AUDIOPATH",)
    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        return (audio_path,)

class LoadSRT:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1] in ["srt", "txt"]]
        return {"required":
                    {"srt": (sorted(files),)},
                }

    CATEGORY = "AIFSH_XTTS"

    RETURN_TYPES = ("SRT",)
    FUNCTION = "load_srt"

    def load_srt(self, srt):
        srt_path = folder_paths.get_annotated_filepath(srt)
        return (srt_path,)