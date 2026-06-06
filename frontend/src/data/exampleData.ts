import { ValidationResult } from '../types/validation';

export const exampleValidationResult: ValidationResult = {
  startup_idea: "An AI-powered platform that helps entrepreneurs validate their startup ideas through comprehensive market analysis, competition research, and risk assessment.",

  market_analysis: {
    customer_segments: [
      {
        segment_name: "Aspiring Entrepreneurs",
        needs: ["Idea validation", "Market insights", "Competitive analysis"],
        motivations: ["Reduce risk of failure", "Make data-driven decisions", "Save time and money"],
        pain_points: ["Lack of market research expertise", "Limited budget for consultants", "Uncertainty about idea viability"],
        sub_segments: ["First-time founders", "Serial entrepreneurs", "Side hustlers"]
      },
      {
        segment_name: "Startup Founders",
        needs: ["Quick market validation", "Competitor insights", "Go-to-market strategy"],
        motivations: ["Pivot faster", "Validate hypotheses", "Impress investors"],
        pain_points: ["Time-consuming research", "Expensive market analysis tools", "Information overload"],
        sub_segments: ["Pre-seed startups", "Seed-stage startups", "Early-stage startups"]
      },
      {
        segment_name: "Students & Researchers",
        needs: ["Academic validation", "Market data", "Trend analysis"],
        motivations: ["Complete coursework", "Research projects", "Entrepreneurship competitions"],
        pain_points: ["Limited access to market data", "Complexity of analysis tools", "Budget constraints"],
        sub_segments: ["MBA students", "Entrepreneurship students", "Academic researchers"]
      }
    ],

    market_size_estimation: {
      segment_estimates: [
        {
          segment: "Aspiring Entrepreneurs",
          population_estimate: "5-10 million globally",
          spending_power: "$50-500 per validation",
          estimated_market_size: "$250M-$5B annually"
        },
        {
          segment: "Startup Founders",
          population_estimate: "2-3 million active startups",
          spending_power: "$100-1000 per validation",
          estimated_market_size: "$200M-$3B annually"
        },
        {
          segment: "Students & Researchers",
          population_estimate: "1-2 million",
          spending_power: "$20-100 per validation",
          estimated_market_size: "$20M-$200M annually"
        }
      ],
      total_addressable_market: "$470M-$8.2B annually",
      realistic_market_size_range: "$500M-$2B (capturing 5-25% of TAM)"
    },

    key_trends: [
      "Rising entrepreneurship culture driven by social media and success stories",
      "Increased adoption of AI and automation tools for business intelligence",
      "Growing demand for lean startup methodologies and rapid validation",
      "Shift towards data-driven decision making in early-stage ventures",
      "Remote work enabling more people to pursue entrepreneurship"
    ],

    opportunities_and_gaps: {
      opportunities: [
        "Underserved market of non-technical founders who need accessible validation tools",
        "Integration with startup ecosystems (accelerators, incubators, universities)",
        "Expansion into adjacent services (pitch deck creation, investor matching)",
        "Global expansion to emerging markets with growing startup ecosystems",
        "API offerings for partners and complementary platforms"
      ],
      gaps: [
        "Most existing tools are expensive and designed for established businesses",
        "Lack of AI-powered, instant feedback mechanisms for idea validation",
        "Limited integration between market research and actionable next steps",
        "No comprehensive platforms combining market, competition, and risk analysis",
        "Insufficient focus on early-stage, pre-funding entrepreneurs"
      ]
    }
  },

  competition_analysis: {
    direct_competitors: [
      {
        name: "IdeaBuddy",
        features: ["Business planning", "Financial forecasting", "Idea validation guides"],
        strengths: ["Comprehensive business planning tools", "User-friendly interface", "Established brand"],
        weaknesses: ["Limited AI capabilities", "Manual data entry required", "Higher pricing tiers"]
      },
      {
        name: "Strategyzer",
        features: ["Business Model Canvas", "Value Proposition Canvas", "Testing tools"],
        strengths: ["Industry-standard frameworks", "Strong educational content", "Enterprise adoption"],
        weaknesses: ["Steep learning curve", "Less automated insights", "Premium pricing"]
      },
      {
        name: "Validator.ai",
        features: ["Idea scoring", "Market feedback", "Competitor tracking"],
        strengths: ["AI-powered insights", "Quick validation", "Community feedback"],
        weaknesses: ["Limited depth of analysis", "Smaller database", "Basic reporting"]
      }
    ],

    indirect_competitors: [
      {
        name: "Google Trends & Market Research Tools",
        category: "Market Research",
        strengths: ["Free access", "Real-time data", "Comprehensive coverage"],
        weaknesses: ["Requires expertise to interpret", "No actionable insights", "Time-consuming"]
      },
      {
        name: "Consulting Firms (McKinsey, BCG)",
        category: "Professional Services",
        strengths: ["Deep expertise", "Customized analysis", "Industry connections"],
        weaknesses: ["Extremely expensive ($50K+)", "Long turnaround time", "Overkill for early-stage"]
      },
      {
        name: "SurveyMonkey & Typeform",
        category: "Survey Tools",
        strengths: ["Easy to use", "Flexible", "Affordable"],
        weaknesses: ["Requires manual analysis", "No market data", "Limited insights"]
      }
    ],

    key_differentiators: [
      "AI-powered instant analysis combining market, competition, and risk assessment",
      "Affordable pricing tiers specifically designed for early-stage entrepreneurs",
      "Actionable recommendations with clear next steps, not just data dumps",
      "Integration of multiple analysis frameworks in one seamless platform",
      "Conversational AI interface that guides users through validation process"
    ],

    strategic_positioning: {
      core_message: "Validate Your Startup Idea in Minutes, Not Months",
      segment_specific_messages: {
        students: "Turn your class project into a real business with AI-powered validation",
        researchers: "Access comprehensive market data and analysis for your entrepreneurship research",
        startup_founders: "Make confident pivot decisions with instant, data-driven insights"
      },
      pricing_strategy: {
        freemium: "Yes - Basic idea validation with limited features (1 analysis per month)",
        tiers: [
          {
            tier_name: "Free",
            target_user: "Students & Explorers",
            pricing: "$0/month",
            features: ["1 idea analysis per month", "Basic market insights", "Community access"]
          },
          {
            tier_name: "Starter",
            target_user: "Aspiring Entrepreneurs",
            pricing: "$29/month",
            features: ["5 idea analyses per month", "Full market & competition reports", "Risk assessment", "Export reports"]
          },
          {
            tier_name: "Professional",
            target_user: "Active Founders",
            pricing: "$99/month",
            features: ["Unlimited analyses", "Advanced AI insights", "Priority support", "API access", "Team collaboration"]
          },
          {
            tier_name: "Enterprise",
            target_user: "Accelerators & Universities",
            pricing: "Custom",
            features: ["White-label solution", "Dedicated support", "Custom integrations", "Analytics dashboard", "Volume discounts"]
          }
        ],
        institutional_pricing: "Special packages for accelerators, incubators, and educational institutions with bulk licenses and custom branding"
      },
      go_to_market_strategy: [
        "Content marketing: SEO-optimized blog posts, YouTube videos on startup validation",
        "Community building: Active presence in startup forums, Reddit, Product Hunt launch",
        "Partnership strategy: Collaborate with accelerators, universities, and startup communities",
        "Freemium model: Low barrier to entry with viral sharing features",
        "Influencer outreach: Target startup influencers and podcasters for reviews and mentions"
      ],
      product_development_focus: [
        "Enhance AI model accuracy with more training data and user feedback loops",
        "Build integrations with popular tools (Notion, Slack, Google Workspace)",
        "Develop mobile app for on-the-go idea validation",
        "Create industry-specific validation templates (SaaS, e-commerce, marketplace, etc.)",
        "Add collaborative features for team-based idea validation and discussion"
      ]
    }
  },

  risk_assessment: {
    market_risks: [
      {
        risk: "Market saturation with AI tools leading to customer fatigue",
        severity: "Medium",
        mitigation: "Focus on specific niche (startup validation) and superior UX; continuous innovation in AI capabilities"
      },
      {
        risk: "Economic downturn reducing discretionary spending on validation tools",
        severity: "Medium",
        mitigation: "Maintain strong freemium tier; demonstrate clear ROI; position as cost-saving alternative to consultants"
      },
      {
        risk: "Changing entrepreneurship trends and startup methodologies",
        severity: "Low",
        mitigation: "Stay agile; regularly update frameworks; engage with startup community for feedback"
      }
    ],

    technical_risks: [
      {
        risk: "AI model producing inaccurate or biased analysis",
        severity: "High",
        mitigation: "Rigorous testing; human review layer; transparent methodology; continuous model improvement; user feedback integration"
      },
      {
        risk: "Data privacy and security concerns with user ideas",
        severity: "High",
        mitigation: "Implement end-to-end encryption; clear privacy policy; SOC 2 compliance; option for private analysis mode"
      },
      {
        risk: "Technical infrastructure scalability issues",
        severity: "Medium",
        mitigation: "Cloud-native architecture; auto-scaling capabilities; performance monitoring; gradual rollout strategy"
      }
    ],

    operational_risks: [
      {
        risk: "Inability to maintain quality with rapid user growth",
        severity: "Medium",
        mitigation: "Automated quality checks; scalable support infrastructure; comprehensive documentation; community forums"
      },
      {
        risk: "Dependence on third-party data sources and APIs",
        severity: "Medium",
        mitigation: "Diversify data sources; build proprietary database; negotiate long-term contracts; have backup providers"
      },
      {
        risk: "Customer acquisition cost exceeding lifetime value",
        severity: "Low",
        mitigation: "Focus on organic growth and word-of-mouth; optimize conversion funnel; increase retention with value-add features"
      }
    ],

    regulatory_risks: [
      {
        risk: "Compliance with data protection regulations (GDPR, CCPA)",
        severity: "High",
        mitigation: "Legal counsel review; privacy-by-design approach; clear terms of service; user consent management; data minimization"
      },
      {
        risk: "Liability for business decisions based on AI recommendations",
        severity: "Medium",
        mitigation: "Clear disclaimers; position as decision-support tool, not definitive advice; E&O insurance; legal terms review"
      },
      {
        risk: "AI regulation compliance (EU AI Act, etc.)",
        severity: "Low",
        mitigation: "Monitor regulatory developments; transparent AI operations; human oversight; compliance-ready architecture"
      }
    ],

    financial_risks: [
      {
        risk: "Insufficient funding to reach profitability",
        severity: "Medium",
        mitigation: "Bootstrap initially; achieve early revenue milestones; demonstrate strong unit economics before raising; maintain lean operations"
      },
      {
        risk: "Revenue concentration in freemium tier with low conversion",
        severity: "Medium",
        mitigation: "Optimize conversion funnel; demonstrate clear value of paid tiers; implement usage-based triggers; offer limited-time upgrades"
      },
      {
        risk: "High infrastructure costs for AI processing",
        severity: "Low",
        mitigation: "Optimize model efficiency; implement caching; negotiate cloud discounts; consider hybrid cloud approach"
      }
    ]
  },

  advisor_recommendations: "Conditional Go",

  advice: "This startup idea shows strong potential with a clear market need and differentiated approach. The AI-powered validation platform addresses real pain points for underserved early-stage entrepreneurs. Key strengths include the growing entrepreneurship trend, gap in affordable validation tools, and scalable AI technology. However, success depends on: (1) developing highly accurate AI models that users trust, (2) acquiring users cost-effectively in a competitive market, (3) converting free users to paid tiers, and (4) maintaining strong data security and privacy. Recommended next steps: Build an MVP focusing on one customer segment (suggest startup founders), validate AI accuracy with pilot users, establish partnerships with 2-3 startup accelerators for initial distribution, and demonstrate strong engagement metrics before significant investment in scaling.",

  messages: [
    "Strong product-market fit potential with clear differentiation",
    "Growing target market driven by entrepreneurship trends",
    "Technical feasibility is high with modern AI capabilities",
    "Revenue model is proven (freemium SaaS)",
    "Focus on trust-building and accuracy will be critical",
    "Consider starting with specific industry verticals (e.g., SaaS validation tool)",
    "Build strategic partnerships early for distribution and credibility",
    "Prioritize user experience and actionable insights over data dumps"
  ]
};
