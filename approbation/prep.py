import pandas as pd
from jiwer import wer
from ua_g2p.preprocessor import PreprocessorG2P

prep = PreprocessorG2P()

def approbate(test_name: str, dataset_path: str) -> None:
    print(f"Approbating {test_name}...\n")

    df = pd.read_csv(dataset_path)
    print(f"Loaded {len(df["text"])} texts from dataset!")
    print("Generating output...\n")
    
    # generate processed texts
    df["ua_g2p"] = [
        " ".join(prep.preprocess_text(txt)).replace("\u0301", "")
        for txt in df["text"]
    ]

    # calculate WER
    ref, hyp = df["reference"].astype(str).tolist(), df["ua_g2p"].astype(str).tolist()
    word_error_rate = wer(ref, hyp) * 100
    word_accuracy = 100 - word_error_rate

    # generate dataframe of mismatches
    mismatch = df[df["reference"] != df["ua_g2p"]]
    if not mismatch.empty:
        report_df = mismatch[["reference", "ua_g2p"]].copy().astype(str)
        for col in report_df.columns:
            max_len = max(report_df[col].str.len().max(), len(col))
            report_df[col] = report_df[col].str.ljust(max_len)
        report_df = f"\n\nErrors on:\n\n{report_df.to_string(index=False, justify="left")}"
    else:
        report_df = "\n\nNo mismatches detected!"

    # generate report
    report = "=" * 120
    report += f"\n\nTotal errors: {len(mismatch["text"])}\n"
    report += f"Word Error Rate: {word_error_rate:.2f}%\nWord Accuracy: {word_accuracy:.2f}%\n\n"
    report += "=" * 120
    report += report_df
    report += "\n\n"
    report += "=" * 120

    print(report)

    print("Saving results...")
    df.to_csv(dataset_path, index=False) # save df to file
    report_fp = f"approbation/output/{test_name.strip().replace(" ", "_")}_report.txt"
    with open(report_fp, "w", encoding="utf-8") as f: # save report to txt
        f.write(report)

    print("Results saved! Check \"approbation/output/\" for report.")

approbate(
        test_name="clitics concatenation",
        dataset_path="approbation/data/preprocessor_test.csv",
    )

