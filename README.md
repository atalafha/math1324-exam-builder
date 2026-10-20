# MATH 1324 Exam Builder

A **static, browser-only** Math for Business exam builder. Choose questions by course section, select multiple-choice or free-response questions, reorder them, and download a compilable `.tex` file using the `exam` document class. No server, account, package manager, or build step required.

## Run locally

Open `index.html` in a browser and click **Load sample questions**. For your real questions, click **Choose File** under **Load question bank** and select your **private** JSON bank.

## Publish to GitHub Pages

1. Create a GitHub repository named `math1324-exam-builder`.
2. Upload `index.html`, `styles.css`, `app.js`, and this README. **Do not upload** any real exam question bank, test ZIP, answer key, or past final.
3. Open **Settings → Pages**, use **Deploy from a branch**, choose **main** and **/(root)**, and save.
4. Open `https://YOUR-USERNAME.github.io/math1324-exam-builder/`.

The source website contains only five *illustrative sample questions*. The real bank is imported locally and is not saved to browser storage or sent to GitHub. Avoid adding confidential questions to the sample source or repository.

## Course topic structure

- Exam 1: 1.1 Simple and Weighted Averages; 1.2 Percents, Ratios, and Proportions; 1.3 Functions; 1.4 Linear Functions; 1.5 Function Transformations; 1.6 Quadratic Functions.
- Exam 2: 2.1 Polynomial Functions; 2.2 Rational Functions; 2.3 Exponential Functions; 2.4 Logarithmic Functions; 2.5 Systems of Equations; 2.6 Augmented Matrices.
- Exam 3: 3.1 Sets, Venn Diagrams, and Cardinality; 3.2 Probability; 3.3 Conditional Probability; 3.4 Counting, Permutations, and Combinations; 3.5 Expected Value.
- Final: cumulative coverage plus 4.1 Linear Inequalities in Two Variables.

Topics follow the uploaded Fall 2026 course materials; some textbook sections may overlap exams depending on the syllabus.

## Private question bank format

Each JSON object has `id`, `exam`, `topic`, `type` (`mc` or `free`), `points`, `difficulty` and `latex`. The `latex` value is the **question body** without `\question[points]`. It may contain a `choices` environment with `\CorrectChoice` and a `solution` environment.

To convert owned Fall 2026 LaTeX exams to a private bank:

```sh
python build_bank.py \
  --exam1 '/path/to/Exam1_1324_F26_VersionA.tex' \
  --exam2 '/path/to/Exam2_1324_F26_VersionA.tex' \
  --output private-question-bank.json
```

**Keep `private-question-bank.json` off public GitHub.** The importer extracts the 12-choice group in Exam 2 as individual 2-point questions. It imports free-response questions as separate entries. The auto-tags are heuristics and **must be reviewed**. Complex shared LaTeX macros and external figure files must be copied or embedded manually for compilation. MC answer shuffling only handles simple `choices` environments. There is no automatic generation of equivalent numerical variants.

## Scope and limitations

- The browser shows source-text previews; it does not render TikZ or compile TeX.
- A download contains `\question` entries in selection order. Individual MC questions have their own numbered questions, rather than the single 24-point umbrella used in the original Exam 2.
- Before distributing exams, check graphics dependencies, wording, point totals, solution output, and that all exported source compiles in Overleaf or another TeX distribution.
- The sample questions are illustrative and are **not** the real uploaded exams.
