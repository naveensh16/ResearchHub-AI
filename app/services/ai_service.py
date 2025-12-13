"""
ResearchHub AI - AI Service for Paper Generation & Review
Supports both OpenAI and Ollama (local LLM)
"""
import os
import json
from flask import current_app

class AIService:
    """AI service for research paper generation and review"""
    
    def __init__(self):
        self.provider = None
        self.client = None
        self.model = None
    
    def _initialize(self):
        """Lazy initialization of AI provider"""
        if self.provider:
            return
        
        self.provider = current_app.config.get('LLM_PROVIDER', 'ollama')
        self.model = current_app.config.get('LLM_MODEL', 'mistral')
        
        if self.provider == 'openai':
            self._init_openai()
        else:
            self._init_ollama()
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            api_key = current_app.config.get('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            self.client = OpenAI(api_key=api_key)
            self.model = self.model or 'gpt-3.5-turbo'
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def _init_ollama(self):
        """Initialize Ollama client"""
        import requests
        self.ollama_url = current_app.config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = self.model or 'mistral'
        
        # Test connection
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print(f"⚠️  Warning: Ollama not responding at {self.ollama_url}")
        except Exception as e:
            print(f"⚠️  Warning: Cannot connect to Ollama: {e}")
    
    def _generate_text(self, prompt, max_tokens=2000):
        """Generate text using configured provider"""
        self._initialize()
        
        if self.provider == 'openai':
            return self._generate_openai(prompt, max_tokens)
        else:
            return self._generate_ollama(prompt, max_tokens)
    
    def _generate_openai(self, prompt, max_tokens):
        """Generate using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert research paper writing assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI generation failed: {str(e)}")
    
    def _generate_ollama(self, prompt, max_tokens):
        """Generate using Ollama"""
        import requests
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                error_detail = ""
                try:
                    error_detail = response.text
                except:
                    pass
                print(f"❌ Ollama error - Status: {response.status_code}, Response: {error_detail}")
                raise Exception(f"Ollama returned status {response.status_code}: {error_detail}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama generation failed: {str(e)}")
    
    def generate_paper_sections(self, title, domain, keywords, objective, method_type, sections):
        """
        Generate multiple paper sections based on inputs
        
        Args:
            title: Paper title
            domain: Research domain
            keywords: Keywords (comma-separated)
            objective: Research objective
            method_type: Methodology type
            sections: List of section names to generate
        
        Returns:
            Dictionary of section_name: generated_content
        """
        generated = {}
        
        base_context = f"""
Research Paper Information:
- Title: {title}
- Domain: {domain}
- Keywords: {keywords}
- Objective: {objective}
- Methodology Type: {method_type}
"""
        
        section_prompts = {
            'abstract': f"""{base_context}
You are an expert academic researcher writing for top-tier conferences (IEEE, ACM, Springer). Generate a publication-quality abstract (250-280 words) that demonstrates deep technical understanding:

STRUCTURE:
1. Context & Motivation (2-3 sentences): Establish the broader field, current challenges, and why this research matters NOW
2. Problem Gap (2 sentences): Identify the specific gap in existing research with technical precision
3. Novel Contribution (3-4 sentences): Clearly articulate what is NEW, DIFFERENT, and SIGNIFICANT about this work. Use strong verbs (propose, introduce, develop, demonstrate)
4. Methodology (2 sentences): Concise technical approach highlighting key innovations
5. Key Results (2-3 sentences): Specific, quantifiable outcomes with comparative improvements (e.g., "achieves 23% improvement over state-of-the-art")
6. Impact (1-2 sentences): Broader implications for research/industry

WRITING STYLE:
- Use sophisticated academic language and domain-specific terminology
- Include quantifiable metrics where possible
- Be assertive about contributions (not tentative)
- Third person, formal tone
- Zero redundancy - every word adds value
- Strong opening sentence that hooks the reader

Make this abstract compelling enough to make reviewers want to read the full paper.""",
            
            'introduction': f"""{base_context}
You are writing the introduction for a TOP-TIER conference paper. Generate 650-750 words that establish authority and expertise:

PARAGRAPH 1 (100-120 words): BROAD CONTEXT & SIGNIFICANCE
- Open with a compelling statement about the field's importance and recent developments
- Cite current trends, market size, or societal impact with specific numbers
- Establish why this research domain matters RIGHT NOW
- Use authoritative tone with strong claims backed by citations [1-3]

PARAGRAPH 2 (90-110 words): TECHNICAL BACKGROUND
- Provide essential technical foundations and key concepts
- Define critical terminology specific to this domain
- Explain the technical landscape briefly
- Reference seminal works [4-6]

PARAGRAPH 3 (100-120 words): EXISTING APPROACHES & LIMITATIONS
- Critically analyze current state-of-the-art methods
- Identify specific technical limitations with examples
- Explain WHY these limitations exist (fundamental constraints, assumptions, trade-offs)
- Use citations [7-10]

PARAGRAPH 4 (90-110 words): RESEARCH GAP & MOTIVATION
- Clearly articulate the gap that others have missed
- Explain the technical challenges in addressing this gap
- Provide concrete examples of failure cases or unmet needs
- Build tension - make the problem feel urgent and important

PARAGRAPH 5 (110-130 words): NOVEL CONTRIBUTIONS
- Bold statement of what THIS work achieves
- List 3-4 specific, technical contributions as bullet points or numbered list
- Emphasize novelty using phrases like "first to...", "unlike previous work...", "uniquely addresses..."
- Quantify improvements where possible

PARAGRAPH 6 (80-100 words): METHODOLOGY PREVIEW
- High-level overview of the approach (not detailed)
- Highlight key technical innovations or insights
- Explain why this approach is better/different
- Tease results without revealing everything

PARAGRAPH 7 (50-70 words): PAPER ORGANIZATION
- Brief roadmap: "The rest of this paper is organized as follows. Section II..."
- Keep formal but concise

WRITING REQUIREMENTS:
- Use sophisticated vocabulary (leverage, paradigm, framework, mechanism, etc.)
- Include 10-15 citation placeholders [1], [2], etc.
- Vary sentence structure - mix short punchy sentences with longer technical ones
- Use transition phrases between paragraphs
- NO casual language or weak phrases ("might", "perhaps", "it is believed")
- Be assertive and confident about contributions
- Technical depth appropriate for domain experts""",
            
            'problem_statement': f"""{base_context}
You are defining the research problem with PRECISION for expert reviewers. Generate 500-550 words:

PARAGRAPH 1 (110-130 words): FORMAL PROBLEM DEFINITION
- Mathematical or precise technical definition of the problem
- State the problem clearly: "Given X, determine Y such that Z is optimized/achieved"
- Explain input/output, constraints, and objectives
- Define scope explicitly (what IS and ISN'T included)
- Use formal language appropriate for the domain

PARAGRAPH 2 (120-140 words): CURRENT STATE-OF-THE-ART ANALYSIS
- Systematically review 3-4 existing approaches
- For EACH: briefly explain the approach, cite [X], and identify its limitation
- Be specific about technical shortcomings (scalability, accuracy, generalization, etc.)
- Use comparative language: "While Method A achieves X, it fails when..."
- Include quantitative limitations where possible (e.g., "limited to datasets under 10K samples")

PARAGRAPH 3 (110-130 words): FUNDAMENTAL TECHNICAL CHALLENGES
- Identify WHY this problem is hard (computational complexity, theoretical barriers, practical constraints)
- Explain conflicting objectives or trade-offs
- Discuss technical challenges that prevent trivial solutions
- Reference complexity analysis if applicable (NP-hard, exponential time, etc.)
- Make it clear why existing solutions are insufficient

PARAGRAPH 4 (90-110 words): RESEARCH GAP & OPPORTUNITY
- Synthesize the above into a clear gap statement
- Explain what's missing from current research
- Identify the theoretical or practical opportunity
- Connect back to the motivation - why filling this gap matters
- Set up YOUR contribution (without revealing solution yet)

PARAGRAPH 5 (70-90 words): SCOPE & BOUNDARIES
- Explicitly state what this research DOES cover
- Clearly state assumptions and limitations
- Define evaluation criteria for success
- Provide context on generalizability

WRITING REQUIREMENTS:
- Technical precision - use domain-specific terminology
- Include 6-10 citations [1], [2], etc.
- Use formal problem statement syntax where appropriate
- Avoid vague language - be specific about numbers, scales, metrics
- Critical analysis, not just description
- Build a logical argument for why this problem needs NEW research""",
            
            'literature_review': f"""{base_context}
You are writing a CRITICAL literature review for expert reviewers. Generate 750-850 words demonstrating deep domain knowledge:

PARAGRAPH 1 (100-120 words): TAXONOMY & ORGANIZATION
- Provide a clear taxonomy of existing approaches
- Categorize methods logically (by technique, by problem formulation, by era, etc.)
- Establish the framework for your review
- Reference survey papers if applicable [1-2]
- Use phrases like "can be broadly categorized into..." or "existing work falls into three paradigms..."

PARAGRAPH 2 (130-150 words): CLASSICAL/FOUNDATIONAL APPROACHES
- Review seminal works from earlier period (pre-2018)
- For 2-3 key methods: explain approach, cite [3-5], analyze strengths AND weaknesses
- Explain their historical importance and why they were state-of-the-art
- Identify fundamental limitations that motivated newer research
- Use transition: "While these classical approaches established..."

PARAGRAPH 3 (130-150 words): MODERN LEARNING-BASED APPROACHES (if relevant)
- Review recent ML/AI-based methods (2019-2022)
- For 2-3 methods: technical details, innovations, citations [6-9]
- Compare performance, computational requirements, data needs
- Critical analysis - don't just describe, EVALUATE
- Highlight what these methods achieved and where they still fall short

PARAGRAPH 4 (130-150 words): CUTTING-EDGE / STATE-OF-THE-ART (2023-2024)
- Review the very latest approaches
- Deep dive into 2-3 most relevant recent works [10-13]
- Explain technical innovations in detail
- Benchmark results if known
- Identify their remaining limitations - this sets up YOUR contribution
- Use critical language: "despite achieving X, these methods struggle with Y because..."

PARAGRAPH 5 (120-140 words): COMPARATIVE ANALYSIS
- Create a critical comparison across approaches
- Discuss trade-offs: accuracy vs speed, simplicity vs performance, generalization vs specialization
- Identify common patterns or fundamental challenges
- Synthesize insights from the literature
- Use a comparative table reference: "Table I summarizes..."

PARAGRAPH 6 (100-120 words): RESEARCH GAPS & DIFFERENTIATION
- Clearly articulate what's MISSING from all reviewed work
- Explain why no existing approach fully solves the problem
- Identify the theoretical or practical gap
- Set up YOUR novel contribution
- Use phrases like "None of the aforementioned approaches address...", "A critical gap remains in..."

WRITING REQUIREMENTS:
- 15-20 citations [1-20] distributed throughout
- Critical, analytical tone - not just descriptive
- Compare and contrast methods explicitly
- Use technical terminology precisely
- Organize chronologically or thematically
- Every citation must have context and critical commentary
- Show deep understanding of methods, not surface-level description
- Use transition phrases between paragraphs for flow
- Make it clear you understand the ENTIRE landscape""",
            
            'methodology': f"""{base_context}
You are writing the TECHNICAL CORE of the paper. Generate 800-900 words with reproducible detail:

SUBSECTION A: RESEARCH DESIGN & FRAMEWORK (150-170 words)
- Present the overall research methodology and theoretical framework
- Explain the rationale for chosen approach (why this methodology fits the problem)
- Provide high-level architecture or system overview
- Reference: "Figure 1 shows the overall framework..."
- Justify design decisions with technical reasoning
- Include formal notation if applicable (define variables, sets, functions)

SUBSECTION B: TECHNICAL APPROACH & ALGORITHM (200-230 words)
- Describe the core algorithm, model, or technique IN DETAIL
- Break down into key steps or components
- Explain novel technical contributions
- Include algorithmic pseudocode reference: "Algorithm 1 presents..."
- Discuss computational complexity if relevant (O(n), O(n²), etc.)
- Explain innovations that differentiate from existing methods
- Use technical terminology precisely
- Define mathematical formulations in text (e.g., "minimize objective function L(θ) = ...")

SUBSECTION C: IMPLEMENTATION DETAILS (150-170 words)
- Programming languages, frameworks, libraries used
- Hardware specifications (if performance-critical)
- Key hyperparameters and their values
- Training procedures, optimization algorithms
- Any preprocessing, normalization, or data augmentation steps
- Specific technical choices with justification
- Reproducibility details (random seeds, initialization, etc.)

SUBSECTION D: EXPERIMENTAL DESIGN (150-170 words)
- Describe datasets used (size, characteristics, source) with citations
- Explain train/validation/test splits or cross-validation strategy
- Baseline methods for comparison with citations [X, Y, Z]
- Experimental variables and controls
- Number of runs, statistical significance testing
- Ablation study design (testing individual components)

SUBSECTION E: EVALUATION METRICS (120-140 words)
- Define ALL metrics used for evaluation
- Explain why each metric is appropriate for this problem
- Include formulas in text: "Precision = TP / (TP + FP)"
- Discuss what constitutes good performance
- Any domain-specific evaluation criteria
- Statistical tests for significance

WRITING REQUIREMENTS:
- Extreme technical precision - experts should be able to reproduce
- Use formal mathematical notation where appropriate
- Include 5-8 citations for datasets, baselines, metrics
- Reference figures, tables, algorithms: "as shown in Figure 2"
- Justify every major decision technically
- Use subsection headings (A, B, C or 1, 2, 3)
- Zero ambiguity - specify exact values, ranges, thresholds
- Balance detail with readability""",
            
            'conclusion': f"""{base_context}
You are writing a STRONG conclusion that reinforces your contributions. Generate 400-450 words:

PARAGRAPH 1 (80-100 words): PROBLEM RECAP
- Briefly restate the research problem (1-2 sentences)
- Remind reader of the research gap and motivation
- Establish context for what was achieved
- Use past tense: "This paper addressed the problem of..."

PARAGRAPH 2 (100-120 words): APPROACH SUMMARY
- Concisely summarize your technical contribution
- Highlight the key innovation or insight
- Explain the core methodology briefly
- Use phrases like "introduced", "proposed", "developed", "demonstrated"
- Emphasize what makes it novel: "Unlike prior work, our approach..."

PARAGRAPH 3 (110-130 words): KEY ACHIEVEMENTS & RESULTS
- State primary findings with SPECIFIC NUMBERS
- Highlight main results: "achieved 95.7% accuracy, surpassing previous best by 8.3%"
- Mention key experimental validations
- Emphasize practical significance
- Be assertive about contributions
- Use power words: "demonstrates", "establishes", "achieves", "advances"

PARAGRAPH 4 (70-90 words): LIMITATIONS & CONSTRAINTS
- Honestly acknowledge limitations of current work
- Scope constraints or assumptions made
- Areas where performance could be improved
- Be balanced - acknowledge without undermining contributions
- Use phrases like "While our approach shows promise, current limitations include..."

PARAGRAPH 5 (80-100 words): BROADER IMPACT & SIGNIFICANCE
- Explain implications for the field
- Potential applications or use cases
- How this advances the research area
- Long-term impact or paradigm shift potential
- Connect back to original motivation
- End with forward-looking statement
- Use impactful language: "This work paves the way for...", "opens new avenues for..."

WRITING REQUIREMENTS:
- Confident, assertive tone about contributions
- Past tense for what was done
- No new information or citations
- Synthesize rather than repeat
- Balance strength with honesty about limitations
- End on an inspiring, forward-looking note
- Every sentence should add value
- No weak phrases ("we believe", "might suggest")""",
            
            'future_work': f"""{base_context}
You are outlining exciting research directions. Generate 300-350 words that inspire continued research:

PARAGRAPH 1 (80-100 words): IMMEDIATE EXTENSIONS
- Specific, concrete improvements planned for short-term
- Address known limitations mentioned in conclusion
- Technical enhancements that directly build on this work
- Be specific: "extend to multi-modal data", "incorporate attention mechanisms", "optimize for mobile deployment"
- Use near-future language: "immediate next steps include..."

PARAGRAPH 2 (90-110 words): LONG-TERM RESEARCH DIRECTIONS
- Broader, more ambitious research avenues
- Theoretical extensions or generalizations
- Integration with other research areas
- Paradigm shifts this work enables
- Use visionary language: "opens possibilities for...", "could lead to..."
- Connect to emerging trends in the field

PARAGRAPH 3 (70-90 words): PRACTICAL APPLICATIONS
- Real-world deployment scenarios
- Industry applications and commercialization potential
- Societal impact and ethical considerations
- Scaling challenges and solutions
- Interdisciplinary collaboration opportunities
- Be concrete about use cases

PARAGRAPH 4 (60-80 words): OPEN QUESTIONS & COMMUNITY CHALLENGES
- Pose thought-provoking questions for the research community
- Identify fundamental challenges that remain
- Call for collaborative research efforts
- Acknowledge what's still unknown
- End with inspiring vision for the future
- Use inclusive language: "we envision", "the community should explore"

WRITING REQUIREMENTS:
- Forward-looking, optimistic tone
- Specific and actionable (not vague "improve performance")
- Balance ambition with feasibility
- Connect to broader research trends
- Show this is a starting point, not an ending
- Inspire others to build on this work
- No citations needed (this is forward-looking)
- Use future tense or modal verbs (will, could, should, may)""",
        }
        
        # Add results section
        section_prompts['results'] = f"""{base_context}
You are presenting COMPELLING research findings. Generate 750-850 words that prove your contribution:

PARAGRAPH 1 (110-130 words): EXPERIMENTAL OVERVIEW
- Summarize the experiments conducted
- State the research questions being answered
- Overview of evaluation methodology
- Mention number of trials, datasets tested, conditions varied
- Set expectations for what follows

PARAGRAPH 2 (140-160 words): QUANTITATIVE RESULTS - PRIMARY METRICS
- Present main performance metrics with SPECIFIC NUMBERS
- Use tables: "Table II presents the comparative results..."
- Show improvements over baselines: "Method X achieves 94.2% accuracy compared to 87.3% for baseline Y, representing a 6.9% absolute improvement"
- Include statistical significance: "p < 0.01"
- Multiple metrics (accuracy, F1-score, speed, memory, etc.)
- Break down by test conditions if applicable

PARAGRAPH 3 (130-150 words): COMPARATIVE ANALYSIS
- Deep comparison with state-of-the-art methods
- Explain WHY your approach performs better
- Discuss trade-offs (if your method is slower but more accurate, justify it)
- Reference visualizations: "Figure 3 illustrates..."
- Identify scenarios where your method excels vs. falls short
- Be honest about limitations while highlighting strengths

PARAGRAPH 4 (120-140 words): ABLATION STUDY & COMPONENT ANALYSIS
- Systematically evaluate contribution of each component
- "To validate the importance of component X, we conducted ablation experiments..."
- Show performance degradation when removing key innovations
- Prove that your novel contributions actually matter
- Include numbers: "Removing feature Y decreased accuracy by 5.2%"

PARAGRAPH 5 (120-140 words): QUALITATIVE ANALYSIS
- Provide insights beyond numbers
- Discuss interesting patterns, failure cases, edge cases
- Include visual examples: "Figure 4 shows representative examples..."
- Explain surprising findings or unexpected behaviors
- Connect results to theoretical expectations

PARAGRAPH 6 (100-120 words): SCALABILITY & EFFICIENCY ANALYSIS
- Runtime performance, memory usage, computational costs
- Scalability to larger datasets or real-world scenarios
- Compare efficiency with baselines
- Discuss practical deployment considerations
- Include graphs: "Figure 5 depicts scalability trends..."

WRITING REQUIREMENTS:
- SPECIFIC NUMBERS everywhere (don't say "improved significantly", say "improved by 12.4%")
- Reference tables and figures: "Table III", "Figure 2"
- Use statistical rigor (confidence intervals, error bars, p-values)
- Be analytical, not just reportive - explain WHY results make sense
- Compare with baselines explicitly
- Acknowledge limitations honestly
- Use strong, confident language for successes
- Include 3-5 citations for comparison methods""",
        
        # Add references section with realistic, high-quality citations
        section_prompts['references'] = f"""{base_context}
Generate 15-20 realistic, high-quality academic references in proper IEEE/ACM format for {domain} research, specifically related to {keywords}.

FORMAT REQUIREMENTS:
Journals (50%): [X] A. Surname, B. Surname, and C. Surname, "Article title in sentence case describing specific technical contribution," Journal Name, vol. X, no. Y, pp. XX-YY, Month Year. DOI: 10.XXXX/YYYYY

Conferences (40%): [X] A. Surname and B. Surname, "Paper title describing technical method or system," in Proc. Conference Name (ACRONYM), City, Country, Year, pp. XX-YY.

Books/Reports (10%): [X] A. Surname, Book Title: Subtitle, Xth ed. City, State: Publisher, Year.

CONTENT REQUIREMENTS:
- Use realistic researcher names (diverse international names)
- Technical titles that reflect actual {domain} research  
- Real venue names (IEEE Transactions, ACM Conferences, Springer journals)
- Recent years (2018-2024, with mix across years)
- Realistic page numbers and DOIs
- Mix of foundational (older) and cutting-edge (recent) references
- Cover the full spectrum: theory, algorithms, applications, surveys
- Include at least 2-3 survey/review papers
- Ensure titles are technically precise and domain-appropriate

EXAMPLES OF QUALITY TITLES:
- "Deep Reinforcement Learning for Autonomous Vehicle Control: A Survey"
- "Efficient Attention Mechanisms for Transformer-Based Language Models"
- "Federated Learning with Differential Privacy: Theory and Practice"
- "Graph Neural Networks: A Review of Methods and Applications"

Make references look authentically academic and properly researched."""
        
        for section in sections:
            if section in section_prompts:
                try:
                    print(f"🤖 Generating {section}...")
                    # Use longer token limits for more detailed generation
                    max_tokens = 1200 if section in ['methodology', 'literature_review', 'introduction'] else 1000
                    if section in ['results', 'conclusion']:
                        max_tokens = 1000
                    elif section in ['abstract', 'problem_statement', 'future_work']:
                        max_tokens = 800
                    elif section == 'references':
                        max_tokens = 1500
                    
                    content = self._generate_text(section_prompts[section], max_tokens=max_tokens)
                    generated[section] = content
                except Exception as e:
                    print(f"❌ Failed to generate {section}: {e}")
                    generated[section] = f"[AI Generation Failed: {str(e)}]\n\nPlease write this section manually."
        
        return generated
    
    def improve_text(self, section_name, current_text, context):
        """
        Improve existing text using AI with publication-quality enhancements
        
        Args:
            section_name: Name of the section
            current_text: Current text content
            context: Dictionary with paper context (title, domain, objective)
        
        Returns:
            Improved text
        """
        prompt = f"""
You are a TOP-TIER academic editor for IEEE/ACM/Springer conferences. Elevate the following {section_name} section to PUBLICATION QUALITY.

Paper Context:
- Title: {context.get('title', 'N/A')}
- Domain: {context.get('domain', 'N/A')}
- Objective: {context.get('objective', 'N/A')}

Current Text:
{current_text}

TRANSFORMATION REQUIREMENTS:

1. TECHNICAL PRECISION
   - Replace vague terms with specific, quantifiable language
   - Add technical depth appropriate for domain experts
   - Use sophisticated domain-specific terminology
   - Include numerical specifics where possible

2. ACADEMIC RIGOR
   - Strengthen arguments with logical flow
   - Add transitional phrases for coherence
   - Use formal academic writing conventions
   - Eliminate casual language, weak verbs, and hedging phrases
   - Replace "we/our" with third person where appropriate

3. CLARITY & CONCISENESS
   - Eliminate redundancy and wordiness
   - Each sentence must add unique value
   - Break overly long sentences
   - Improve paragraph structure and flow

4. PROFESSIONAL POLISH
   - Fix all grammatical errors
   - Ensure consistent tense and voice
   - Improve sentence variety and rhythm
   - Add power words (demonstrate, establish, achieve, introduce)

5. CONFERENCE-STANDARD FORMATTING
   - Proper citations format [1], [2] if applicable
   - Reference figures/tables correctly
   - Use appropriate section structure
   - Maintain formal tone throughout

6. CONTENT ENHANCEMENT
   - Strengthen weak claims with specifics
   - Add depth without changing core meaning
   - Improve examples and explanations
   - Make contributions/results more compelling

OUTPUT REQUIREMENTS:
- Return ONLY the improved text
- NO explanations, NO meta-commentary
- Maintain the original length ±20%
- Preserve all technical facts and contributions
- Elevate quality to top conference standards

Transform this text into publication-ready content that would impress expert reviewers."""
        
        print(f"🔍 Improve request - Section: {section_name}, Text length: {len(current_text)} chars")
        print(f"🔍 Prompt length: {len(prompt)} chars")
        
        return self._generate_text(prompt, max_tokens=1200)
    
    def review_paper(self, paper):
        """
        Review paper for issues and provide feedback
        
        Args:
            paper: Paper model instance
        
        Returns:
            Dictionary with review results
        """
        # Collect all sections
        sections_content = f"""
Paper: {paper.title}

Abstract: {paper.abstract or '[Missing]'}

Introduction: {paper.introduction or '[Missing]'}

Problem Statement: {paper.problem_statement or '[Missing]'}

Literature Review: {paper.literature_review or '[Missing]'}

Methodology: {paper.methodology or '[Missing]'}

Conclusion: {paper.conclusion or '[Missing]'}

Future Work: {paper.future_work or '[Missing]'}
"""
        
        prompt = f"""
You are an expert research paper reviewer. Analyze this paper and identify issues:

{sections_content}

Provide a JSON response with the following structure:
{{
    "overall_score": <1-10>,
    "findings": [
        {{
            "type": "<structure|clarity|logic|completeness>",
            "severity": "<low|medium|high|critical>",
            "section": "<section name>",
            "issue": "<description>",
            "suggestion": "<improvement suggestion>"
        }}
    ],
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<improvement 1>", "<improvement 2>"]
}}

Check for:
1. Missing sections
2. Weak or unclear arguments
3. Logical inconsistencies
4. Structure problems
5. Clarity issues
6. Incomplete content

Return ONLY valid JSON, no other text."""
        
        try:
            response = self._generate_text(prompt, max_tokens=1500)
            
            # Try to parse JSON
            # Clean response (remove markdown code blocks if present)
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                response = response.split('```')[1].split('```')[0].strip()
            
            review_data = json.loads(response)
            return review_data
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "overall_score": 5,
                "findings": [
                    {
                        "type": "completeness",
                        "severity": "medium",
                        "section": "general",
                        "issue": "AI review generated non-JSON response",
                        "suggestion": "Manual review recommended"
                    }
                ],
                "strengths": ["Paper structure present"],
                "improvements": ["Review content manually", "Ensure all sections are complete"]
            }
        except Exception as e:
            print(f"Review error: {e}")
            return {
                "overall_score": 5,
                "findings": [
                    {
                        "type": "error",
                        "severity": "high",
                        "section": "general",
                        "issue": f"Review failed: {str(e)}",
                        "suggestion": "Try again or review manually"
                    }
                ],
                "strengths": [],
                "improvements": []
            }
