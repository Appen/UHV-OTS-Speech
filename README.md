# About
This repository provides data and code for the paper:

**[Scalable Data Annotation Pipeline for High-Quality Large Speech Datasets Development](https://openreview.net/forum?id=-OFOwaDriw7)** (submitted to NeurIPS 2021 Track on Datasets and Benchmarks Round2)

**Authors**: Mingkuan Liu, Chi Zhang, Hua Xing, Chao Feng, Monchu Chen, Judith Bishop, Grace Ngapo

**Keywords**: speech processing, speech dataset, human in the loop, annotation pipeline, quality assurance, speech annotation

# Abstract
This paper introduces a human-in-the-loop (HITL) data annotation pipeline to generate high-quality, large-scale speech datasets. The pipeline combines human and machine advantages to more quickly, accurately, and cost-effectively annotate datasets with machine pre-labeling and fully manual auditing. Quality control mechanisms such as blind testing, behavior monitoring, and data validation have been adopted in the annotation pipeline to mitigate potential bias introduced by machine-generated labels. Our A/B testing and pilot results demonstrated the HITL pipeline can improve annotation speed and capacity by at least 80\% and quality is comparable to or higher than manual double pass annotation. We are leveraging this scalable pipeline to create and continuously grow ultra-high volume off-the-shelf (UHV-OTS) speech corpora for multiple languages, with the capability to expand to 10,000+ hours per language annually. Customized datasets can be produced from the UHV-OTS corpora using dynamic packaging. UHV-OTS is a long-term Appen project to support commercial and academic research data needs in speech processing. Appen will donate a number of free speech datasets from the UHV-OTS each year to support academic and open source community research under the CC-BY-SA license. We are also releasing the code of the data pre-processing and pre-tagging pipeline under the Apache 2.0 license to allow reproduction of the results reported in the paper. Code and data are available in https://github.com/Appen/UHV-OTS-Speech

![](./DataPipeline.png)
**HITL speech corpora development system pipeline for UHV-OTS corpora**

# Reproduce the automated machine pre-labeling results reported in the paper

## 0. Experiment envirionments setup
```bash

```  

## 1. Data pre-filtering: synthetic speech detection

Reference. Cite original paper & code.

```bash

```  

## 2. Data pre-processing: music/vocal source separation

We utilized well performed [spleeter](https://github.com/deezer/spleeter) library for source separation. The spleeter is source separation library of [Deezer](https://www.deezer.com/) and was introduced in ["Spleeter: a fast and efficient music source separation tool with pre-trained models"](https://www.researchgate.net/publication/342429039_Spleeter_a_fast_and_efficient_music_source_separation_tool_with_pre-trained_models). We post the script to run this tool on web scraped audio files. To run the tool with sample file, please run following command in docker container.


```bash
cd /opt/scripts/source_separation

```  

## 3. Data pre-filtering: language/accent identification
Reference. Cite original paper & code.


```bash

```  

## 4. Data pre-tagging: speech detection
Reference. Cite original paper & code.


```bash

```  

## 5. Data pre-tagging: speaker segmentation
Reference. Cite original paper & code.


```bash

```  

## 6. Data pre-tagging: speaker clustering & identification
Reference. Cite original paper & code.


```bash

```  

## 7. Data pre-tagging: gender detection

Reference. Cite original paper & code.


```bash

```  


## 8. Data pre-tagging: speech recognition/transcription

Reference. Cite original paper & code.


```bash

```  

## 9. Data pre-tagging: domain/topic detection

Reference. Cite original paper & code.


```bash

```  

# UHV-OTS dataset format

# Sample codes to parse/convert UHV-OTS data format to Kaldi style data format

# Speech Annotation Instruction

The whole pipeline will automatically generate abundant types of tags and transcriptions on the collected audio data. The human-in-the-loop scheme enroll native language speaker as human annotator to audit all the automatical tags and transcriptions and correct if necessary. In our SaaS platform client.appen.com, we set up audit jobs for native language spoken workers to do review and finalize the annotation.  The instructions provide to them is show in below:

**OTS Automation- Annotation Job**

**Overview**

Listen to a short piece of audio and transcribe the text.

**We Provide**

- A short piece of audio
- A text box to enter the transcription
**Process**
 - Step 1: Listen to the audio
 - Step 2: Verify audio tags
    - Choose the noise type of the speech in the audio
    - Determine whether the speech of entire audio is in US English
    - Determine whether there is only one speaker or more in the audio
    - Determine the gender of speaker if there is only one speaker
    - Determine the whether the content in this Audio is offensive
 - Step 3: Review and Correct Audio Transcription
    Review the transcription in text box, correct it if necessary.

Enter text as all lowercase. No capitalization. 
If portions of the spoken audio are not clear, insert the \[unclear\] tags 

### Thank You!


**Notes on Transcriptions**

This batch contains a hypothesis in the text box. Edit the transcription to match the audio.

  - Please pay particular attention to correcting the use of similar-sounding words: **hi/high**, **there/their**, etc.

Many of the calls are about medical emergencies. You may hear some disturbing content. Remember that you can always abandon a batch if you are uncomfortable with its content.

  - Use the **\[unclear\]**  if the speech is not intelligible .
  - Use the **\[no-speech\]** tag if there is no speech  in the audio.
  - Use the **\[noise\]** tag if there is no speech but only noise in the audio.
  - Use the **\[music\]** tag if there is no speech but only music/song  in the audio.

### Transcription Rules and Tips
| Category | Audio Clip | Correct Transcription |
| -------- | ---------- | --------------------- |
| **Stutter•** Transcribe the word that the user is intending to say | What t-time is it |	what time is it  |
| **Hesitation•** Don’t transcribe hesitations• Don’t transcribe interjections• Don’t transcribe fragments	| Pull up um Spotify He mhm he pull up Spo-Spotify	| pull up spotify he pull up spotify |
| **Self-correction•** When the user self-corrects, transcribe everything the user says	Will would you open spotify	will would you open spotify |
| **Numerals•** Words or phrases should be the spelled-out version	891 oh 2 |	eighty nine one o two |
| **Time and Date Phrases•** Words or phrases should be transcribed as the user says |	7:00 1/2/2019	| seven o’clock january second twenty nineteen (or january second two thousand nineteen based on the audio |
| **Contractions•** When encountering contractions, do not split the contraction into two words. We should be transcribeing exactly what we hear	| i'm gonna leave i'm going to leave	| i'm gonna leave i'm going to leave |
| **Acronyms•** Acronyms that are pronounced as an actual word instead of as a sequence of letters will be transcribed as one word |	NASA SCUBA |	nasa scuba |


**Pronunciation**

  - Speakers often pronounce his as “he’s”. This is just the accent, so it should still be transcribed as his
  - Listen carefully for the difference between “curve” and “curb”. Because of the nature of these calls, it’s much more likely for speakers to be talking about curbs
  - The term **repo order** is pronounced like “ree-poh”
  - People will often say **they gone** when speakers of other dialects might say “they’ve gone” or “they left”. Transcribe the words exactly as they are spoken
  - **we'll** and **will** may sound closer to each other than in other accents you’re used to. Make sure you are using the correct one
  - **that’s** may sound more like “thass” or “dass”. Be sure to still transcribe it as **that’s**
  - When someone is saying the letter “L” (when spelling out a word), it can sound like “eyol”
  - **address** can sound a bit like “edges”. Be sure to spell it **address** in that case
  - **phone** can sound like “fuh-wan” or “fowan”. Be sure not to accidentally transcribe it as a word like “following”

**Grammar**

  - Use a period at the end of sentences, especially if a different speaker starts talking after that
  - Be mindful of the difference between your (possession) and you’re (you are)
  - Be mindful of the difference between its (possession) and it’s (contraction of “it is”) and be sure you are using the right one
  - Please spell okay rather than “ok”
  - Keep in mind the difference between their (possession) and they’re (contraction of “they are”) and make sure you are using the right one
  - Bear in mind the difference between suites and sweets, which are pronounced the same. If the person is talking about a hotel or other location, the correct spelling will most likely be suites
  - If a speaker says something like “buh-bye” please transcribe it as bye bye


###Thank you for your work on this task!
```


# License

## Software license

MIT or Apache 2 license

## Dataset license

CC-BY-SA for future

Here is the list
- item 1
- item 2


Here is the task list

- [x] done item1
- [ ] wip item 2

# References
