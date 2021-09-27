
# UHV-OTS dataset format with detailed samples

The UHV-OTS speech corpora combine speech audio, corresponding transcriptions, acoustic event tagging and speech/audio/speaker-related metadata such as accent, background noise, topic, domain, gender etc. Those detailed metadata are presented at utterance, session, speaker, and dataset levels as below samples in the format of JSON. 

##  Dataset level meta data
This metadata contains language, accent, speaker-related demographic information, topics and audio distribution statistics at the level of the entire dataset.
A typical sample UHV-OTS speech dataset level metadata JSON file as below.

UHV-OTS-Commercial-enus-general-lighthouse-2021XXXX.json=
```json
{
   "speechdb_name":"UHV-OTS-Commercial-enus-general-lighthouse-2021XXXX",
   "language":  "english",
   "accent": "en-us",
   "duration_in_hours": 210,
   "speakers_cnt":  310, 
   "utterances_cnt": 53418,
   "Topics_by_hours": {               
        "sports":20.5, 
        "culture":53.5, 
        "education":46.4, 
        "finance":30.6, 
        "food":59
    },
   "Topics_by_speakers": {               
        "sports":52, 
        "culture":76, 
        "education":50, 
        "finance":48, 
        "food":84
    },
   "gender_dist_by_hours": { "male": 117.5, "female": 92.5}, 
   "gender_dist_by_speakers": { "male": 164, "female": 146}, 
   "noisetype_dist_by_hours":  {"clean": 35, "noisy": 105, "music":70},  
   "sampling_rate": 16000, 
   "sampling_bit": 16, 
   "audio_channels": 1 
} 
```

## Session level meta data
An audio session is a group of related utterances, for example, an hour-long audio clip of an interview. All session level metadata contains information such as session_id, speakers, audio_path, duration, utterance_ids_list, domains, topics, and accents. A typical sample session level metadata JSON file with session\_id="asd123efs" as below.

asd123efs.json=
```json
{ 
    "session_id": "asd123efs",
    "audio_path": "/audio-session/asd123efs.mp3", 
    "duration_in_minutes": 35.7, 
    "utterance_ids_list": ["asd123efs-1", ..., "asd123efs-28" ], 
    "speakers" : ["sddseewsf32sxeor", "sadflk23laevs"], 
    "session brief title": "nba sports news westbrook", 
    "domains": ["sports"],  
    "topics": ["sports", "basketball", "nba"], 
    "language": "English", 
    "accent": "en-us", 
    "noise_background": "noisy", 
    "sampling_rate": 16000, 
    "sampling_bit": 16
} 
```


##  Utterance level meta data

An utterance is a short audio clip, usually comprising a single spoken sentence of no more than 20 seconds' duration. All metadata at the utterance level has information such as path to the audio file, speaker ID, speaker accent, speaker gender, text transcription, audio length, session\_id, topics and background noise type.  A typical sample utterance level metadata JSON file with utterce\_id="asd123efs-123" as below.

asd123efs-123.json=
```json
{ 
    "utterce_id": "asd123efs-123", 
    "speaker_id": "sddseewsf32sxeor", 
    "session_id": "asd123efs", 
    "audio_path": "/audio-utterance/asd123efs/asd123efs-123.mp3",
    "duration_in_seconds": 15.3,
    "domains": ["sports"],
    "topics": ["sports", "basketball", "nba"],
    "tx_lexical": "westbrook had thirty five points fourteen rebounds and twenty one assists to lead washington to a win",
    "tx_display": "Westbrook had 35 points, 14 rebounds and 21 assists to lead Washington to a win.",
    "language": "English",
    "accent": "en-us",
    "gender":  "male",
    "noise_background": "noisy", 
    "sampling_rate": 16000,
    "sampling_bit": 16
} 
```

## Speaker level meta data

Every speaker has a metadata file which contains information about speaker ID, accent, gender, language, list of utterance\_ids, list of session\_ids, and the duration of audio from this speaker. To ensure highly diversified speakers in the corpora, audio from the same speaker is limited to less than 60 minutes. A typical sample utterance level metadata JSON file with speaker\_id="sddseewsf32sxeor" as below.

sddseewsf32sxeor.json=
```json
{ 
	"speaker_id": "sddseewsf32sxeor", 
	"utterce_ids_list": ["asd123efs-11", "asd123efs-23","weadsffdsa-321",... ], 
	"context_ids_list": ["asd123efs", "weadsffdsa"], 
	"duration_in_minutes": 45.3,  
	"language": "English", 
	"accent": "en-us", 
	"gender":  "male", 
}
```