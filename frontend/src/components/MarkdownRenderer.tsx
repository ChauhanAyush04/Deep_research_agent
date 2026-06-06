import React from "react";
import ReactMarkdown from "react-markdown";
import { AlertCircle, Lightbulb, Shield } from "lucide-react";
import remarkGfm from "remark-gfm";

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  const components = {
    // Main title
    h1: (props: any) => (
      <h1 
        className="text-5xl font-bold text-gray-900 mt-12 mb-8 leading-tight" 
        {...props} 
      />
    ),

    // Section headers
    h2: (props: any) => (
      <h2 
        className="text-3xl font-bold text-gray-900 mt-10 mb-6 pb-3 border-b-2 border-blue-200" 
        {...props} 
      />
    ),

    // Subsection headers
    h3: (props: any) => (
      <h3 
        className="text-2xl font-bold text-gray-800 mt-8 mb-4" 
        {...props} 
      />
    ),

    // Regular paragraphs
    p: (props: any) => (
      <p 
        className="text-gray-700 leading-8 mb-6 text-lg" 
        {...props} 
      />
    ),

    // Unordered lists
    ul: (props: any) => (
      <ul className="space-y-3 my-6 ml-6" {...props} />
    ),

    // Ordered lists
    ol: (props: any) => (
      <ol className="space-y-3 my-6 ml-6 list-decimal" {...props} />
    ),

    // List items
    li: (props: any) => (
      <li 
        className="text-gray-700 leading-relaxed" 
        {...props} 
      />
    ),

    // Bold text - as badges/highlights
    strong: ({ children }: any) => (
      <span className="font-bold text-gray-900 bg-yellow-100 px-2 py-1 rounded">
        {children}
      </span>
    ),

    // Italic text
    em: ({ children }: any) => (
      <em className="italic text-gray-700">{children}</em>
    ),

    // Block quotes - for important notes
    blockquote: ({ children }: any) => {
      const text = String(children).toLowerCase();
      let bgColor = "bg-blue-50 border-blue-200 text-blue-900";
      let Icon = Lightbulb;

      if (text.includes("limitation") || text.includes("challenge")) {
        bgColor = "bg-amber-50 border-amber-200 text-amber-900";
        Icon = AlertCircle;
      }
      if (text.includes("important") || text.includes("critical")) {
        bgColor = "bg-red-50 border-red-200 text-red-900";
        Icon = Shield;
      }

      return (
        <div className={`border-l-4 p-6 rounded-lg my-8 flex gap-4 ${bgColor}`}>
          <Icon className="w-6 h-6 flex-shrink-0 mt-1" />
          <div className="leading-relaxed">{children}</div>
        </div>
      );
    },

    // Code blocks
    code: ({ inline, className, children }: any) => {
      if (inline) {
        return (
          <code className="bg-gray-200 px-2 py-1 rounded text-sm font-mono text-gray-800">
            {children}
          </code>
        );
      }
      return (
        <pre className="bg-gray-900 text-gray-100 p-6 rounded-lg my-6 overflow-x-auto">
          <code className="font-mono text-sm">{children}</code>
        </pre>
      );
    },

    // Links
    a: ({ href, children }: any) => (
      <a 
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 underline font-medium"
      >
        {children}
      </a>
    ),

    // Tables
    table: (props: any) => (
      <div className="my-8 rounded-lg border border-gray-200 overflow-hidden shadow-sm">
        <table className="w-full text-sm" {...props} />
      </div>
    ),

    // Table headers
    th: (props: any) => (
      <th
        className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider text-white bg-gradient-to-r from-gray-700 to-gray-800"
        {...props}
      />
    ),

    // Table cells
    td: (props: any) => (
      <td 
        className="px-6 py-4 text-gray-700 border-t border-gray-200" 
        {...props} 
      />
    ),

    // Horizontal rule
    hr: () => (
      <hr className="my-12 border-t-2 border-gray-300" />
    ),
  };

  return (
    <div className="prose prose-lg max-w-none">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </ReactMarkdown>
    </div>
  );
};