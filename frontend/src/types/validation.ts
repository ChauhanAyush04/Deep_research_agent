export interface ValidationResult {
  topic: string;
  research_questions: string[];
  research_topics: string[];
  web_findings: WebFinding[];
  top_5_papers: Paper[];
  final_report: string;
}

export interface WebFinding {
  question: string;
  summary: string;
  sources: Source[];
}

export interface Source {
  title: string;
  url: string;
  type: string;
}

export interface Paper {
  title: string;
  authors: string[];
  year: number;
  summary: string;
  key_findings: string[];
  limitations: string[];
  url: string;
  relevance_score: number;
  citation_count: number;
}