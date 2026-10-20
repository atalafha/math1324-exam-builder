"""Run locally to create a private JSON bank from instructor-owned exam source files."""
import json,re,argparse
from pathlib import Path
TOPICS={
'Exam 1':['1.1 Simple and Weighted Averages','1.2 Percents, Ratios, and Proportions','1.3 Functions','1.4 Linear Functions','1.5 Function Transformations','1.6 Quadratic Functions'],
'Exam 2':['2.1 Polynomial Functions','2.2 Rational Functions','2.3 Exponential Functions','2.4 Logarithmic Functions','2.5 Systems of Equations','2.6 Augmented Matrices'],
'Exam 3':['3.1 Sets, Venn Diagrams, and Cardinality','3.2 Probability','3.3 Conditional Probability','3.4 Counting, Permutations, and Combinations','3.5 Expected Value'],
'Final':['4.1 Linear Inequalities in Two Variables']}

def classify(text, exam):
 t=text.lower()
 patterns={
 '1.1':['weighted','average','mean'], '1.2':['percent','ratio','proportion','discount'], '1.3':['domain','range','function','evaluate'], '1.4':['linear','slope','break-even','revenue'], '1.5':['transform','shift','translation','reflect'], '1.6':['quadratic','vertex','parabola'],
 '2.1':['polynomial','multiplicity','end behavior','factor'], '2.2':['rational','asymptote','average cost','hole'], '2.3':['exponential','compound','depreci','growth','interest'], '2.4':['logarithm','log(','log_','\\ln'], '2.5':['system','elimination','substitution'], '2.6':['matrix','row reduc','augmented'],
 '3.1':['venn','cardinality','union','intersection','sets'], '3.2':['probability','dice','die','coin'], '3.3':['conditional','independent','given that'], '3.4':['permutation','combination','ways','arrangements'], '3.5':['expected','prize','payoff'], '4.1':['inequalit','feasible region','constraint']}
 choices=[x for x in TOPICS.get(exam,[]) if x.split()[0] in patterns]
 scored=[(sum(t.count(w) for w in patterns[x.split()[0]]),x) for x in choices]
 return max(scored,key=lambda a:a[0])[1] if scored else 'Uncategorized'

def split_questions(source):
 body=source.split(r'\begin{questions}',1)[-1].split(r'\end{questions}',1)[0]
 parts=re.split(r'(?m)^\s*\\question(?:\[(\d+)\])?',body)
 return [(int(parts[i] or 0),parts[i+1].strip()) for i in range(1,len(parts),2)]

def extract(path,exam,version='A'):
 s=Path(path).read_text(encoding='utf-8',errors='replace'); result=[]
 for index,(points,body) in enumerate(split_questions(s),1):
  # The Exam 2 MC block has \part entries with nested choices. Extract those as separate standalone questions.
  if r'\begin{choices}' in body and r'\begin{parts}' in body:
   parts_region=body.split(r'\begin{parts}',1)[1].split(r'\end{parts}',1)[0]
   chunks=re.split(r'(?m)^\s*\\part\s+',parts_region)[1:]
   if chunks and all(r'\begin{choices}' in c for c in chunks):
    for j,c in enumerate(chunks,1):
     tex=c.strip(); result.append(dict(id=f'{exam.replace(" ","")}-{version}-{index:02d}-{j:02d}',exam=exam,topic=classify(tex,exam),type='mc',difficulty='Medium',points=points//len(chunks) if points else 2,latex=tex,source=Path(path).name,version=version))
    continue
  tex=body.strip();result.append(dict(id=f'{exam.replace(" ","")}-{version}-{index:02d}',exam=exam,topic=classify(tex,exam),type='free',difficulty='Medium',points=points or 5,latex=tex,source=Path(path).name,version=version))
 return result

def main():
 a=argparse.ArgumentParser();a.add_argument('--exam1',required=True);a.add_argument('--exam2',required=True);a.add_argument('--output',default='private-question-bank.json');args=a.parse_args()
 bank=extract(args.exam1,'Exam 1')+extract(args.exam2,'Exam 2')
 Path(args.output).write_text(json.dumps(bank,indent=2,ensure_ascii=False),encoding='utf-8')
 print(f'Created {len(bank)} questions at {args.output}. Keep this file private; do not commit it to GitHub.')
if __name__=='__main__':main()
