# About
This repository provides data and code for the paper:

**[Scalable Data Annotation Pipeline for High-Quality Large Speech Datasets Development](https://openreview.net/forum?id=-OFOwaDriw7)** (submitted to NeurIPS 2021 Track on Datasets and Benchmarks Round2)

**Authors**: Mingkuan Liu, Chi Zhang, Hua Xing, Chao Feng, Monchu Chen, Judith Bishop, Grace Ngapo

# Abstract
This paper introduces a human-in-the-loop (HITL) data annotation pipeline to generate high-quality, large-scale speech datasets. The pipeline combines human and machine advantages to more quickly, accurately, and cost-effectively annotate datasets with machine pre-labeling and fully manual auditing. Quality control mechanisms such as blind testing, behavior monitoring, and data validation have been adopted in the annotation pipeline to mitigate potential bias introduced by machine-generated labels. Our A/B testing and pilot results demonstrated the HITL pipeline can improve annotation speed and capacity by at least 80\% and quality is comparable to or higher than manual double pass annotation. We are leveraging this scalable pipeline to create and continuously grow ultra-high volume off-the-shelf (UHV-OTS) speech corpora for multiple languages, with the capability to expand to 10,000+ hours per language annually. Customized datasets can be produced from the UHV-OTS corpora using dynamic packaging. UHV-OTS is a long-term Appen project to support commercial and academic research data needs in speech processing. Appen will donate a number of free speech datasets from the UHV-OTS each year to support academic and open source community research under the CC-BY-SA license. We also release the code of the data pre-processing and pre-tagging pipeline to allow reproduce of the reported results in the paper under MIT license. Code and data are available in https://github.com/Appen/UHV-OTS-Speech.

![](./DataPipeline.png)
**HITL speech corpora development system pipeline for UHV-OTS corpora**

# Reproduce the results reported in the paper

## 0. Experiment envirionments setup
```bash

```  

## 1. Data pre-filtering: synthetic speech detection
```bash

```  

## 2. Data pre-processing: music/vocal source separation
```bash

```  

## 3. Data pre-filtering: language/accent identification
```bash

```  

## 4. Data pre-tagging: speech detection
```bash

```  

## 5. Data pre-tagging: speaker segmentation
```bash

```  

## 6. Data pre-tagging: speaker clustering & identification
```bash

```  

## 7. Data pre-tagging: gender detection
```bash

```  

## 8. Data pre-tagging: age-group detection
```bash

```  

## 9. Data pre-tagging: speech recognition/transcription
```bash

```  

## 10. Data pre-tagging: domain/topic detection
```bash

```  

# UHV-OTS dataset format

# Sample codes to parse/convert UHV-OTS data format to Kaldi style data format



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

