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


### Thank you for your work on this task!

