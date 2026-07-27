#!/usr/bin/env python3
"""Generate PDF study summaries from lecture slide content."""

from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "pdfs"
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# Each lecture: title + list of (section_heading, [bullet, ...])
LECTURES: list[dict] = [
    {
        "id": "L01",
        "file": "L01_Introduction.pdf",
        "title": "L01 — Introduction",
        "subtitle": "Course overview and digital character pipeline",
        "sections": [
            ("Course goals", [
                "Build conversational digital characters end-to-end",
                "Speech recognition, LLM responses, speech synthesis, animation",
                "Autonomous agents, personality, and emotions",
            ]),
            ("Assessment", [
                "Written exam: 120 minutes, 120 points, no summary sheet",
                "Non-programmable calculator and neutral dictionary allowed",
                "Optional quizzes in 7 lectures: 25/35 correct → +0.25 grade bonus",
            ]),
            ("Pipeline architecture", [
                "User speech → Speech Recognition → transcript",
                "Transcript + emotion/intention/personality → Chatbot (LLM or dialogue tree)",
                "Response text → Speech Synthesis + Animation Synthesis",
                "Feedback loop: user emotion detected from text, speech, video",
            ]),
            ("Course topics (lecture map)", [
                "Affective Computing → Deep Learning → Speech Recognition",
                "LLMs (3 lectures) → Speech Synthesis (2) → Animation (2)",
                "Autonomous Agents → Applications → Reinforcement Learning",
            ]),
            ("Use cases", [
                "Digital Einstein: ETH branding, chatbot + TTS + animation",
                "Healthcare, education, museums, metaverse companions",
                "Location-based and mixed-reality experiences",
            ]),
            ("Speech synthesis history (preview)", [
                "Concatenative → statistical parametric → neural end-to-end",
                "Training costs of modern LLMs are substantial (industry context)",
            ]),
        ],
    },
    {
        "id": "L02",
        "file": "L02_Affective_Computing.pdf",
        "title": "L02 — Affective Computing",
        "subtitle": "Emotion theory, video features, and biosensors",
        "sections": [
            ("What is affect?", [
                "Broader than emotion: moods, attitudes, interpersonal stances",
                "Three ingredients of human behavior: cognition, affect, behavior",
                "Applications: education (learning gain), health, digital characters",
            ]),
            ("Emotion theories", [
                "James-Lange: Stimulus → physiological response → emotion (sequential)",
                "Cannon-Bard: physiological arousal and emotion occur simultaneously",
                "Schachter-Singer: arousal + cognitive interpretation → emotion",
                "Dimensional: valence, arousal, dominance (Russell's core affect)",
                "Basic emotions (Ekman): joy, sadness, disgust, surprise, anger, fear",
            ]),
            ("Video-based recognition", [
                "Pipeline: preprocessing → feature extraction → classification (valence/arousal)",
                "Action Units (FACS): 46 AUs, independent facial muscle motions",
                "Examples: Happiness = AU6+12; Surprise = AU1+2+5+26",
                "Eye blinks: AU45 per frame; Eye gaze: 9 regions",
                "Mouth Aspect Ratio: MAR = (|p2-p8|+|p3-p7|+|p4-p6|) / (3·|p5-p1|)",
                "Fidgeting: frame diff → threshold → energy % → background update",
                "Classifiers: Random Forest, SVM, TCNs, Transformers, CNNs on face images",
            ]),
            ("Biosensors", [
                "ECG: electrical heart activity from skin electrodes",
                "PPG: light reflected by blood vessels (also via webcam)",
                "HRV: std of R-R intervals, RMSSD, pNN50; higher HRV → relaxed/adaptive",
                "Skin conductance (GSR): sweating level, indicative of arousal",
                "SC decomposition: phasic (event-related) + tonic (baseline) via convex optimization (cvxEDA)",
                "Phasic features: amplitude, latency, rise time, half-recovery time",
            ]),
            ("Artifact detection (R-R intervals)", [
                "QD = (Q3 - Q1) / 2",
                "MAD = (Median Beat - 2.9·QD) / 3",
                "MED = 3.32·QD",
                "CBD = (MAD + MED) / 2",
                "Beat is artifact if |RR - last_valid| > CBD",
            ]),
            ("Ground truth", [
                "Self-Assessment Manikin (SAM): valence, arousal, dominance",
                "Other sensors: EEG, EMG, respiration",
            ]),
        ],
    },
    {
        "id": "L03",
        "file": "L03_Deep_Learning.pdf",
        "title": "L03 — Deep Learning Preliminaries",
        "subtitle": "Neural nets, RNNs, attention, and Transformers",
        "sections": [
            ("Neural network unit", [
                "z = w·x + b; output a = σ(z)",
                "Activations: ReLU (most common), sigmoid [0,1], tanh [-1,1]",
                "Softmax: converts logits to probabilities summing to 1",
                "Training: forward pass → loss (cross-entropy) → backpropagation",
            ]),
            ("Feedforward networks", [
                "Input → hidden (ReLU) → output (sigmoid or softmax)",
                "Applications: sentiment classification, language modeling",
            ]),
            ("Recurrent Neural Networks", [
                "h_t = σ(U·h_{t-1} + W·x_t); y_t = f(V·h_t)",
                "Shared weights U, V, W across time steps; processed sequentially",
                "Captures sequential data via hidden state memory",
                "Vanishing gradient problem limits long-range dependencies",
                "LSTM: forget, input, output gates + cell state highway",
                "Bidirectional RNN: left-to-right + right-to-left, concatenate hidden states",
                "Stacked RNNs: multiple layers for richer representations",
                "Uses: language modeling, sentiment classification (last hidden state), generation",
                "Teacher forcing: use gold previous token during training",
            ]),
            ("Encoder-decoder", [
                "Encoder summarizes input (x1…xT) into context vector h_T",
                "Decoder generates output sequence autoregressively",
                "Applications: machine translation, summarization, dialogue",
                "p(y|x) = product of conditional next-token probabilities",
            ]),
            ("Attention mechanism", [
                "Problem: RNN bottleneck and vanishing gradients for long sequences",
                "Score: sim(q, k_t) = q·k_t / sqrt(d) [scaled dot-product]",
                "Weights: a_t = softmax(scores); Context: c = Σ a_t · v_t",
                "Self-attention: Q, K, V from same sequence",
                "Cross-attention: Q from decoder, K/V from encoder",
                "Multi-head attention: multiple parallel attention heads",
            ]),
            ("Transformers", [
                "No inherent order → positional encoding added to embeddings",
                "PE(t,2i) = sin(t/10000^(2i/d)); PE(t,2i+1) = cos(t/10000^(2i/d))",
                "Encoder: multi-head self-attention + FFN + skip connections + layer norm",
                "Decoder: masked self-attention (no future peeking) + cross-attention",
                "Layer norm: normalize across sequence per example (not batch norm)",
            ]),
        ],
    },
    {
        "id": "L04",
        "file": "L04_Speech_Recognition.pdf",
        "title": "L04 — Speech Recognition",
        "subtitle": "Phonetics, features, ASR architectures, and WER",
        "sections": [
            ("Phonetics", [
                "Phones: speech sounds (ARPAbet/IPA symbols)",
                "F0 = lowest frequency of periodic waveform; pitch = perceptual correlate",
                "Mel scale: Mel = 1127·ln(1 + f/700) — perceptual pitch spacing",
                "Complex waves = sum of sine waves; spectrogram shows frequency over time",
                "Consonant types: fricatives, stops; vowels have formant structure",
            ]),
            ("Feature extraction pipeline", [
                "1. Windowing: 20-40 ms frames, ~50% overlap, Hamming window",
                "2. DFT/FFT per frame → power spectrum P(k)",
                "3. Mel filter bank: triangular overlapping filters on Mel scale",
                "4. Log mel → ~80-dimensional feature vector per frame",
                "Augmentation: time warping, frequency masking, time masking",
            ]),
            ("Mel filter bank construction", [
                "Convert f_low and f_high to Mel",
                "Space N+2 points linearly in Mel (for N filters)",
                "Convert back to Hz; create triangular filters (start-peak-end)",
            ]),
            ("ASR architectures", [
                "Encoder-decoder with subsampling (CNN pooling, pyramidal RNN)",
                "CTC: per-frame output + blank token; collapse duplicates; alignment via dynamic programming",
                "RNN-Transducer: encoder + predictor (LM) + joiner; supports streaming",
                "Streaming: increment output u on non-blank, acoustic index t on blank",
                "Whisper: Transformer encoder-decoder, multilingual multitask",
            ]),
            ("Word Error Rate", [
                "WER = 100 × (Substitutions + Insertions + Deletions) / N_ref",
                "Lower is better; function-word errors common",
                "Statistical significance: matched-pair sentence segment word error test",
            ]),
        ],
    },
    {
        "id": "L05",
        "file": "L05_Chatbot_I.pdf",
        "title": "L05 — Chatbot I: Foundations",
        "subtitle": "NLP, embeddings, generation, and LLM adaptation",
        "sections": [
            ("Chatbot basics", [
                "Definition: program simulating human conversation (AI not required)",
                "Rule-based: deterministic, precise, low risk; poor scalability/flexibility",
                "Retrieval vs generation: encoder-encoder (dot product) vs encoder-decoder",
            ]),
            ("Text representation", [
                "Tokenization: BPE sub-word tokens",
                "BoW → tf-idf → dense embeddings (Word2Vec, GloVe)",
                "Encoder models (BERT): bidirectional, good for understanding",
                "Decoder models (GPT): autoregressive, good for generation",
            ]),
            ("Response generation", [
                "Language model: P(x_{t+1} | x_1, …, x_t)",
                "Greedy: always highest prob (repetitive)",
                "Top-k: sample from k most likely tokens",
                "Top-p (nucleus): smallest set with cumulative prob ≥ p",
                "Temperature: sharpens/flattens distribution",
                "Beam search: keep top-B partial hypotheses",
            ]),
            ("LLM adaptation", [
                "Fine-tuning: update weights on task data (needs compute + data)",
                "Prompt engineering: in-context examples, no weight updates",
                "Instruction tuning (FLAN/T5), MMLU multitask pretraining",
                "RLHF: reward model + policy optimization (InstructGPT/ChatGPT)",
                "Prompting: zero-shot, few-shot, chain-of-thought, self-ask, ReAct",
            ]),
            ("Optimizations", [
                "PEFT / LoRA: train low-rank adapters, freeze most weights",
                "Pruning: remove least important weights",
                "Knowledge distillation: teacher → smaller student",
                "Quantization: lower precision (AWQ, SmoothQuant)",
            ]),
        ],
    },
    {
        "id": "L06",
        "file": "L06_Chatbot_II.pdf",
        "title": "L06 — Chatbot II",
        "subtitle": "Prompting, RAG, and chatbot evaluation",
        "sections": [
            ("Prompting", [
                "Roles: system (persona), user (input), assistant (history)",
                "In-context learning: examples at inference, no gradient updates",
                "Structured outputs: JSON schema, function calling / tool use",
                "ReAct: Thought → Action → Observation loop",
                "DSPy: automatic few-shot example selection",
            ]),
            ("Retrieval Augmented Generation (RAG)", [
                "Solves: hallucination, stale/private knowledge",
                "Pipeline: chunk documents → embed → retrieve → augment prompt → generate",
                "Chunking: fixed-size, recursive, semantic",
                "Sparse retrieval: tf-idf, BM25 + inverted index",
                "Dense retrieval: bi-encoder (SBERT), ColBERT (token MaxSim)",
                "Vector DBs: FAISS, Pinecone, Milvus, Weaviate (ANN search)",
                "Reranking: bi-encoder (fast, top-100) → cross-encoder (precise, top-5)",
                "Evaluation: grounding score, answer relevance",
            ]),
            ("Chatbot evaluation", [
                "Qualitative: MOS (1-5 rating), A/B preference tests",
                "Quantitative: perplexity, BLEU, cosine similarity",
                "Perplexity: P = 2^(-1/N · Σ log2 P(w_i)) — lower is better",
                "LLM-as-a-Judge: strong LLM rates responses",
                "Benchmarks: Chatbot Arena (Elo), MMLU, Stanford HELM",
            ]),
        ],
    },
    {
        "id": "L07",
        "file": "L07_Chatbot_III.pdf",
        "title": "L07 — Chatbot III: Multimodality",
        "subtitle": "Multimodal input, emotion recognition, personality",
        "sections": [
            ("Full interaction pipeline", [
                "Speech-to-text → feature recognition → user state → response generation",
                "→ chatbot state → speech synthesis + animation",
                "User state: emotion, attention, age, gender, appearance, etc.",
            ]),
            ("Emotion recognition", [
                "Taxonomies: VAD (dimensional) vs basic emotions (categorical)",
                "Visual: landmarks → CNN (VGG, EfficientNet) or ViT/Swin",
                "Audio: pitch, rhythm, intonation, energy from Mel spectrogram",
                "FACS for facial action units",
                "Fusion: early (concatenate features), late (fuse predictions), hybrid",
            ]),
            ("Multimodal models", [
                "CLIP: contrastive text-image pre-training, shared embedding space",
                "VLMs: joint visual + text processing (e.g. LLaVA)",
                "Personalization: user-specific fine-tuning on labeled data",
            ]),
            ("Personality modeling", [
                "Human Big Five (OCEAN): openness, conscientiousness, extraversion, agreeableness, neuroticism",
                "Chatbot traits: artificiality, conscientiousness, vibrancy, civility, neuroticism",
                "Dynamic Personality Infusion: trait intensity (-2 to +2) rewrites LLM response",
            ]),
        ],
    },
    {
        "id": "L08",
        "file": "L08_Speech_Synthesis_I.pdf",
        "title": "L08 — Speech Synthesis I",
        "subtitle": "Text analysis, prosody, diphone and unit selection",
        "sections": [
            ("TTS pipeline overview", [
                "Stage 1: Text Analysis (normalization, phonetics, prosody)",
                "Stage 2: Waveform Synthesis (concatenative or parametric)",
            ]),
            ("Text normalization", [
                "Identify tokens → chunk sentences → classify types → expand to words",
                "Handles: abbreviations, numbers, punctuation disambiguation",
                "Homographs: live/li:v/ vs /laiv/ via POS tagging + dictionary",
            ]),
            ("Phonetic analysis", [
                "CMUdict: ~127K words, 39 phonemes, stress markers 0/1/2",
                "G2P: ML classifier for out-of-vocabulary words",
                "Names: ~20% of tokens; morphology and rhyme rules",
            ]),
            ("Prosodic analysis", [
                "Prominence/accent: which syllable is stressed in context",
                "Boundaries: intonation phrase (||), intermediate phrase (|)",
                "Duration and F0 (fundamental frequency) per phone",
                "Stress = lexical (fixed in word); accent = context-dependent",
                "Prominence classes: unaccented, reduced, pitch accent, nuclear accent",
                "ToBI: H* (peak), L* (low), L-H% (continuation rise)",
            ]),
            ("Diphone synthesis", [
                "Diphone: half of each adjacent phone — captures coarticulation",
                "Record → segment → concatenate with Hanning window → prosody modify",
                "Epoch labeling: vocal fold cycle markers (Praat)",
            ]),
            ("Unit selection synthesis", [
                "Larger units from ~10h recorded speech; minimal signal processing",
                "Target cost T(s_t, u_j): match F0, stress, duration, position",
                "Join cost J(u_j, u_{j+1}): smoothness at boundaries (=0 if consecutive in DB)",
                "Select sequence minimizing sum of target + join costs",
            ]),
        ],
    },
    {
        "id": "L09",
        "file": "L09_Speech_Synthesis_II.pdf",
        "title": "L09 — Speech Synthesis II",
        "subtitle": "Acoustic models, vocoders, style transfer",
        "sections": [
            ("Modern neural TTS", [
                "Text analysis → Acoustic model (mel spectrogram) → Vocoder (waveform)",
            ]),
            ("Tacotron 2", [
                "Encoder: char embedding + conv layers + bi-LSTM",
                "Autoregressive decoder with attention → mel frames",
                "Postnet refines mel spectrogram",
                "Pros: high quality; Cons: slow, attention instability (skip/repeat)",
            ]),
            ("FastSpeech / FastSpeech 2", [
                "Non-autoregressive: duration predictor + length regulator",
                "Parallel decoding → fast inference, stable output",
                "FastSpeech 2: variance predictors for duration, energy, pitch",
                "Speed control: scale duration D (2×D → half speed)",
                "Uni-TTS: multilingual FastSpeech 2 base (Microsoft Azure)",
            ]),
            ("Vocoders", [
                "Griffin-Lim: iterative phase from magnitude, no training, robotic",
                "WaveNet: autoregressive dilated causal convolutions, high quality, slow",
                "HiFi-GAN: GAN with multi-scale + multi-period discriminators, real-time",
                "DiffWave: diffusion-based, high quality, slow inference",
                "HiFi-GAN losses: adversarial + feature matching + L1 mel loss",
            ]),
            ("Style / speaker control", [
                "One-hot speaker labels vs learned speaker embeddings",
                "Embeddings enable interpolation and zero-shot adaptation",
                "Style tokens: unsupervised style discovery",
            ]),
            ("Evaluation", [
                "MOS: 1-5 naturalness rating; A/B preference tests",
                "DRT: 96 rhyming pairs in carrier phrases",
                "MRT: 50 sets of 6 similar words",
                "WER via ASR on synthesized speech (intelligibility)",
            ]),
        ],
    },
    {
        "id": "L10",
        "file": "L10_Animation_I.pdf",
        "title": "L10 — Animation I",
        "subtitle": "Principles, anatomy, kinematics, and skinning",
        "sections": [
            ("Character fundamentals", [
                "Stylized vs realistic: stylized avoids uncanny valley",
                "Uncanny valley: appeal drops as human-likeness increases (before real human)",
            ]),
            ("Disney's 12 principles (know for exam)", [
                "1. Squash and Stretch — mass and rigidity",
                "2. Anticipation — preparation before main action",
                "3. Staging — clear focus",
                "4. Straight Ahead vs Pose to Pose",
                "5. Follow Through and Overlapping Action",
                "6. Slow In and Slow Out — ease in/out (NOT linear)",
                "7. Arc — natural curved paths",
                "8. Secondary Action",
                "9. Timing",
                "10. Exaggeration",
                "11. Solid Drawing",
                "12. Appeal",
            ]),
            ("Anatomy and rigging", [
                "Facial muscles: bone-to-skin; wrinkles perpendicular to contraction",
                "Joints: hinge, ball-and-socket, etc.; 0-6 degrees of freedom",
                "Skeleton hierarchy: bones define movement, joints define rotation",
            ]),
            ("Kinematics", [
                "Forward kinematics (FK): joint angles → end-effector position",
                "Inverse kinematics (IK): target position → joint angles",
                "Jacobian method: Δθ = α · J⁺ · Δe",
                "Pole vector: controls elbow/knee bend direction in IK",
                "Mass-spring systems for secondary motion",
            ]),
            ("Skinning", [
                "Linear Blend Skinning (LBS): v' = Σ w_ij · (R_j · v_i + T_j)",
                "Each vertex influenced by multiple bones with weights summing to 1",
                "Candy-wrapper artifact: unnatural twisting at large joint angles",
                "Motion capture: blend weights per vertex",
            ]),
        ],
    },
    {
        "id": "L11",
        "file": "L11_Animation_II.pdf",
        "title": "L11 — Animation II",
        "subtitle": "Data-driven animation and speech-driven faces",
        "sections": [
            ("Why ML for animation?", [
                "MoCap cannot cover all possible chatbot responses",
                "Procedural methods are repetitive; need on-the-fly synthesis",
                "Active listening: generate plausible non-speaker animations with context",
            ]),
            ("Datasets", [
                "BIWI 3D, MEAD, VOCASET: 3D face scans with emotion",
                "IEMOCAP: dyadic dialogs, multi-modal, 9 emotions + VAD",
                "BEAT, Talking with Hands: co-speech gestures",
            ]),
            ("Learning-based methods", [
                "Holden's methods: phase-functioned neural networks for locomotion",
                "DeepPhase: phase-aware autoencoder for periodic motion manifolds",
                "Normalizing flows: invertible maps, exact likelihood via Jacobian determinant",
                "Applications: diverse motion generation with temporal consistency",
            ]),
            ("Speech-driven animation", [
                "Procedural: amplitude from audio waveform",
                "FaceFormer: transformer for speech-driven 3D facial animation",
                "Blendshapes: brow, eyes, jaw, mouth controls",
            ]),
            ("Evaluation", [
                "FID: realism of generated motion distribution",
                "Foot sliding / contact error for locomotion",
            ]),
        ],
    },
    {
        "id": "L12",
        "file": "L12_Autonomous_Agents.pdf",
        "title": "L12 — Autonomous Agents",
        "subtitle": "Agent properties, dialogue trees, and knowledge graphs",
        "sections": [
            ("Agent definition and properties", [
                "Agent: perceives environment via sensors, acts via actuators",
                "Reactivity: timely response to environmental changes",
                "Autonomy: operates without direct human control",
                "Proactiveness: plans for future opportunities (not just reacting)",
                "Socially intelligent agents: real-time perception, emotion, action in social settings",
            ]),
            ("Decision-making approaches", [
                "Finite State Machines: states + transition conditions",
                "Dialogue trees: hierarchical choices; low flexibility, hard to scale",
                "LLM-based: task decomposition, tool use, continuous interaction",
            ]),
            ("Knowledge graphs", [
                "RDF triples: (subject, predicate, object)",
                "Schema design with typed entities and relations",
                "SPARQL: W3C standard query language for structured retrieval",
                "Query types: one-hop, path, conjunctive",
            ]),
            ("Knowledge graph embeddings", [
                "TransE: h + r ≈ t; score = ||h + r - t||",
                "TransE limitation: symmetric relations (r ≈ 0)",
                "TransR: entities and relations in different spaces",
                "Link prediction: infer missing edges in large/incomplete graphs",
                "Query2box: box embeddings for complex conjunctive queries",
            ]),
            ("LLM + KG integration", [
                "KG grounds LLM facts; reduces hallucination",
                "Use cases: smart home coordination, healthcare, recommendations, bias mitigation",
            ]),
        ],
    },
    {
        "id": "L13",
        "file": "L13_Applications.pdf",
        "title": "L13 — Metrics & Applications",
        "subtitle": "Evaluation, ethics, and case studies",
        "sections": [
            ("TTS evaluation (recap)", [
                "MOS, A/B tests, DRT, MRT, WER for intelligibility",
            ]),
            ("Responsible AI", [
                "Harmful system: negative real-world impact",
                "Biased system: different performance across subpopulations",
                "Bias sources: training data, system design, distribution shift",
                "ASR racial disparities; face recognition demographic bias",
                "Problem formulation should be ethical (e.g. predict criminality from face = bad task)",
            ]),
            ("Case studies", [
                "Digital Einstein: image generation, upcoming leg/feet animation",
                "Virtual Doctor: experimental user study setup",
                "Virtual Psychotherapist: human vs AI therapist evaluation",
            ]),
            ("Exam preparation", [
                "Review all pipeline components and evaluation metrics",
                "Know trade-offs: rule-based vs LLM, concatenative vs neural TTS, etc.",
            ]),
        ],
    },
    {
        "id": "L14",
        "file": "L14_Reinforcement_Learning.pdf",
        "title": "L14 — Reinforcement Learning",
        "subtitle": "MDPs, policy optimization, and behavior synthesis",
        "sections": [
            ("ML paradigms", [
                "Supervised: (data, label) pairs, backpropagation",
                "Unsupervised: learn latent representations (autoencoders)",
                "RL: agent-environment interaction, reward signal (no labels)",
                "RL for non-differentiable simulators (physics, game engines)",
            ]),
            ("MDP and key concepts", [
                "State s, action a, reward r, policy π(a|s), return R (discounted sum)",
                "Trajectory τ: sequence of (s, a, r) from one episode",
                "Markov property: future depends only on current state",
            ]),
            ("Value functions", [
                "Q(s,a): expected return from taking action a in state s",
                "V(s): E_{a~π}[Q(s,a)]",
                "Optimal policy maximizes expected return (not each individual reward)",
            ]),
            ("Algorithms", [
                "Policy gradient: optimize π directly via sampled trajectories",
                "Actor-Critic: critic baseline reduces variance",
                "PPO: clipped surrogate objective, on-policy rollouts",
                "Q-learning: implicit policy = argmax_a Q(s,a); off-policy with replay buffer",
                "Reward does NOT need to be differentiable",
            ]),
            ("PPO advantages", [
                "Critic baseline reduces variance",
                "Clipped surrogate prevents destructively large policy updates",
                "Multiple epochs on same batch improves sample efficiency",
            ]),
            ("Behavior synthesis applications", [
                "Humanoid locomotion and goal reaching",
                "Soccer dribbling, motion tracking in simulation",
                "Formulate: state, action, reward, policy for each task",
                "Prior knowledge (e.g. z ~ N(0,I)) can be encoded as KL penalty",
            ]),
        ],
    },
]


class SummaryPDF(FPDF):
    def __init__(self, lecture: dict):
        super().__init__()
        self.lecture = lecture
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ArialUni", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self.lecture["title"], align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("ArialUni", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"AI for Digital Characters — {self.page_no()}", align="C")

    def write_title_page(self):
        self.add_page()
        self.set_font("ArialUni", "B", 20)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 12, self.lecture["title"])
        self.ln(4)
        self.set_font("ArialUni", "", 13)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 8, self.lecture["subtitle"])
        self.ln(6)
        self.set_font("ArialUni", "I", 10)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 6, "Study summary generated from lecture slides. ETH AI for Digital Characters.")
        self.ln(8)

    def write_section(self, heading: str, bullets: list[str]):
        self.set_font("ArialUni", "B", 12)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 8, heading)
        self.ln(2)
        self.set_font("ArialUni", "", 10)
        self.set_text_color(30, 30, 30)
        for bullet in bullets:
            self.set_x(self.l_margin + 2)
            self.multi_cell(0, 5.5, f"  •  {bullet}")
        self.ln(4)


def sanitize(text: str) -> str:
    """Replace characters that may not render in PDF."""
    replacements = {
        "→": "->",
        "←": "<-",
        "≥": ">=",
        "≤": "<=",
        "Σ": "sum",
        "σ": "sigma",
        "π": "pi",
        "θ": "theta",
        "α": "alpha",
        "β": "beta",
        "γ": "gamma",
        "Δ": "Delta",
        "·": "*",
        "×": "x",
        "≈": "~",
        "≠": "!=",
        "⁺": "+",
        "⁻": "-",
        "₂": "2",
        "₁": "1",
        "₀": "0",
        "₃": "3",
        "ᵢ": "i",
        "ₜ": "t",
        "—": "-",
        "–": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def build_pdf(lecture: dict, out_path: Path) -> None:
    pdf = SummaryPDF(lecture)
    pdf.add_font("ArialUni", "", FONT)
    pdf.add_font("ArialUni", "B", FONT)
    pdf.add_font("ArialUni", "I", FONT)
    pdf.set_font("ArialUni", "", 10)

    pdf.write_title_page()
    for heading, bullets in lecture["sections"]:
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.write_section(sanitize(heading), [sanitize(b) for b in bullets])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))


def build_combined_pdf(out_path: Path) -> None:
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_font("ArialUni", "", FONT)
    pdf.add_font("ArialUni", "B", FONT)
    pdf.add_font("ArialUni", "I", FONT)
    pdf.set_auto_page_break(auto=True, margin=18)

    pdf.add_page()
    pdf.set_font("ArialUni", "B", 22)
    pdf.set_text_color(20, 40, 80)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 12, "AI for Digital Characters")
    pdf.ln(4)
    pdf.set_font("ArialUni", "", 14)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 8, "Lecture Slide Summaries (L01-L14)")
    pdf.ln(8)
    pdf.set_font("ArialUni", "", 11)
    for lec in LECTURES:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 7, sanitize(f"{lec['id']}: {lec['subtitle']}"))

    for lecture in LECTURES:
        pdf.add_page()
        pdf.set_font("ArialUni", "B", 16)
        pdf.set_text_color(20, 40, 80)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 10, sanitize(lecture["title"]))
        pdf.ln(2)
        pdf.set_font("ArialUni", "I", 11)
        pdf.set_text_color(80, 80, 80)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 7, sanitize(lecture["subtitle"]))
        pdf.ln(6)
        for heading, bullets in lecture["sections"]:
            if pdf.get_y() > 255:
                pdf.add_page()
            pdf.set_font("ArialUni", "B", 11)
            pdf.set_text_color(20, 40, 80)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.epw, 7, sanitize(heading))
            pdf.ln(1)
            pdf.set_font("ArialUni", "", 9)
            pdf.set_text_color(30, 30, 30)
            for bullet in bullets:
                pdf.set_x(pdf.l_margin + 2)
                pdf.multi_cell(pdf.epw - 2, 5, f"- {sanitize(bullet)}")
            pdf.ln(3)

    pdf.output(str(out_path))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lecture in LECTURES:
        path = OUT_DIR / lecture["file"]
        build_pdf(lecture, path)
        print(f"Wrote {path}")

    combined = OUT_DIR / "ALL_Lectures_Summary.pdf"
    build_combined_pdf(combined)
    print(f"Wrote {combined}")


if __name__ == "__main__":
    main()
