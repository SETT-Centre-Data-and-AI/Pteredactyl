## Background

We introduce a concentrated validation battery to the open-source OHDSI community, a Python module for cPII redaction on free text, and a web application that compares various models against the battery. This setup, which allows simultaneous production API deployment using  Gradio, is remarkably efficient and can operate on a single CPU core.

### Methods:

We evaluated three open-source models from Huggingface: Stanford Base De-Identifier, Deberta PII, and Nikhilrk De-Identify using our Clinical_PII_Redaction_Test dataset. The text was tokenised, and all entities such as [PERSON], [ID], and [LOCATION] were tagged in the gold standard. Each model redacted cPII from clinical texts, and outputs were compared to the gold standard template to calculate the confusion matrix, accuracy, precision, recall, and F1 score.

### Results

The full results of the tool are given below in <i>Table 1</i> below.

| Metric     | Stanford Base De-Identifier | Deberta PII | Nikhilrk De-Identify |
|------------|-----------------------------|-------------|----------------------|
| Accuracy   | 0.98                        | 0.85        | 0.68                 |
| Precision  | 0.91                        | 0.93        | 0.28                 |
| Recall     | 0.94                        | 0.16        | 0.49                 |
| F1 Score   | 0.93                        | 0.28        | 0.36                 |

<small><i>Table 1: Summary of Model Performance Metrics</i></small>

### Strengths
- The test benchmark [Clinical_PII_Redaction_Test](https://huggingface.co/datasets/MattStammers/Clinical_PII_Redaction_Test) intentionally exploits commonly observed weaknesses in NLP cPII token masking systems such as clinician/patient/diagnosis name similarity and commonly observed ID/username and location/postcode issues.

- [The Stanford De-Identifier Base Model](https://huggingface.co/StanfordAIMI/stanford-deidentifier-base)[1] is 99% accurate on our test set of radiology reports and achieves an F1 score of 93% on our challenging open-source benchmark. The others models are really to demonstrate the potential of Pteredactyl to deploy any transfomer model.

- We have submitted the code to [OHDSI](https://www.ohdsi.org/) as an abstract and aim strongly to incorporate this into a wider open-source effort to solve intractable clinical informatics problems.

### Limitations
- The tool was not designed initially to redact clinic letters as it was developed primarily on radiology reports in the US. We have made some augmentations to cover elements like postcodes using checksums but these might not always work. The same is true of NHS numbers as illustrated above.

- It may overly aggressively redact text because it was built as a research tool where precision is prized > recall. However, in our experience this is uncommon enough that it is still very useful.

- This is very much a research tool and should not be relied upon as a catch-all in any production-type capacity. The app makes the limitations very transparently obvious via the attached confusion matrix.

### Conclusion
The validation cohort introduced in this study proves to be a highly effective tool for discriminating the performance of open-source cPII redaction models. Intentionally exploiting common weaknesses in cNLP token masking systems offers a more rigorous cPII benchmark than many larger datasets provide.

We invite the open-source community to collaborate to improve the present results and enhance the robustness of cPII redaction methods by building on the work we have begun [here](https://github.com/SETT-Centre-Data-and-AI/PteRedactyl).

### References:
1. Chambon PJ, Wu C, Steinkamp JM, Adleberg J, Cook TS, Langlotz CP. Automated deidentification of radiology reports combining transformer and “hide in plain sight” rule-based methods. J Am Med Inform Assoc. 2023 Feb 1;30(2):318–28.
2. Kotevski DP, Smee RI, Field M, Nemes YN, Broadley K, Vajdic CM. Evaluation of an automated Presidio anonymisation model for unstructured radiation oncology electronic medical records in an Australian setting. Int J Med Inf. 2022 Dec 1;168:104880.