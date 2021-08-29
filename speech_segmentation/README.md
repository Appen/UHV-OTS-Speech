This is the folder containing the demo scripts of speech segmentation. The speech segmentation in this folder is adopted from the InaSpeechSegmenter which was introduced in [AN OPEN-SOURCE SPEAKER GENDER DETECTION FRAMEWORK FOR MONITORING GENDER EQUALITY](https://hal.archives-ouvertes.fr/hal-01927560/document). We only used the speech detection module of it  and it's pretrained model. 

The inaSpeechSegmenter system won the first place in the Music and/or Speech Detection in Music Information Retrieval Evaluation eXchange 2018 (MIREX 2018). This module also achieved 97.5\% detection accuracy with an average boundary mismatch of 97ms at Appen's proprietary testset. To run demo of this module, please run the following command:
```bash
cd speech_detection
./run_demo.sh
``` 
