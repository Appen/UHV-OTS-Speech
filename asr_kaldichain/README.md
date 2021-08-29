To run the experiments on Librispeech test-clean and test-other data with our own Chain model, please run the following command.

```bash
cd /opt/asr_kaldichain
./download_prepare_extract.sh
```

The test-clean and test-other data will be downloaded inside the container. 

In this module, we trained our own ASR model using Kaldi toolkit, specifically using the chain model recipe. But we trained our model using 11 corpora at hand, including free public corpora, purchased corpora, and self owned corpora.

To run the test on Librispeech test-other and test-clean data with our trained model, please run the following command.

```bash
./run_test.sh
```
