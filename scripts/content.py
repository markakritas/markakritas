"""Everything that shows up on the profile, kept apart from the drawing code.

Edit freely: `build.py` re-renders every figure from these tables.
"""

from datetime import date


USER = "markakritas"
NAME = "Mark Akritas"
ROLE = "data scientist · ml & ai engineer"
TAGLINE = "fitting models to a noisy universe."

# header key/value block
FACTS = [
    ("now", "ai/ml engineer"),
    ("focus", "llms · rag · agents · voice ai"),
    ("codes", "python · r · sql · js"),
    ("speaks", "hy · en · ru · el"),
    ("base", "yerevan, armenia"),
]

CONTACTS = [
    # (chip label, chip value, href) — href lives in README.md
    ("mail", "markakrita@gmail.com"),
    ("web", "markakritas.github.io"),
]

# ── projects ──────────────────────────────────────────────────────────────
NEWSLETTER = {
    "name": "NewsPEPper",
    "kicker": "weekly python newsletter",
    "about": "PEPs and Python releases, summarized every saturday.",
    "feed": "https://newspepper.dev/feed.xml",
}
PHILOSOPHY = {
    "name": "map of philosophy",
    "about": "a tool for philosophy enthusiasts",
    "status": "in development",
}
EXTENSION = ("jumpwise", "vs code extension")

# decoration for the philosophy card: thinkers in rough chronological order,
# and who read whom
THINKERS = [
    "heraclitus",
    "parmenides",
    "socrates",
    "plato",
    "aristotle",
    "augustine",
    "aquinas",
    "descartes",
    "spinoza",
    "hume",
    "kant",
    "schopenhauer",
    "nietzsche",
    "wittgenstein",
]
INFLUENCES = [
    ("heraclitus", "plato"),
    ("parmenides", "plato"),
    ("socrates", "plato"),
    ("plato", "aristotle"),
    ("plato", "augustine"),
    ("aristotle", "aquinas"),
    ("augustine", "aquinas"),
    ("aquinas", "descartes"),
    ("descartes", "spinoza"),
    ("hume", "kant"),
    ("kant", "schopenhauer"),
    ("schopenhauer", "nietzsche"),
    ("spinoza", "nietzsche"),
    ("schopenhauer", "wittgenstein"),
]

# ── periodic table of tools ───────────────────────────────────────────────
# family -> (legend label, palette color)
FAMILIES = {
    "lang": ("languages", "yellow"),
    "model": ("modelling", "red"),
    "llm": ("llm stack", "purple"),
    "voice": ("voice ai", "aqua"),
    "ship": ("shipping", "blue"),
    "noble": ("noble gases", "green"),
    "tool": ("tooling", "muted"),
}

# (row, col, symbol, name, family); rows 1–3 mimic the real table's silhouette,
# row 4 is the detached f-block underneath.
ELEMENTS = [
    (1, 1, "Py", "Python", "lang"),
    (1, 12, "Lx", "Linux", "noble"),
    (2, 1, "R", "R", "lang"),
    (2, 2, "Sq", "SQL", "lang"),
    (2, 7, "vL", "vLLM", "llm"),
    (2, 8, "Rg", "RAG", "llm"),
    (2, 9, "Wv", "Weaviate", "llm"),
    (2, 10, "Kz", "kreuzberg", "llm"),
    (2, 11, "Sx", "SearXNG", "llm"),
    (2, 12, "Dk", "Docker", "noble"),
    (3, 1, "Js", "JavaScript", "lang"),
    (3, 2, "Sh", "Shell", "lang"),
    (3, 3, "Pt", "PyTorch", "model"),
    (3, 4, "Sk", "scikit-learn", "model"),
    (3, 5, "Lr", "LoRA", "model"),
    (3, 6, "Mx", "mixed models", "model"),
    (3, 7, "Lk", "LiveKit", "voice"),
    (3, 8, "El", "ElevenLabs", "voice"),
    (3, 9, "Dg", "Deepgram", "voice"),
    (3, 10, "Ap", "REST APIs", "ship"),
    (3, 11, "Db", "Dashboards", "ship"),
    (3, 12, "Gt", "Git", "noble"),
    (4, 4, "Uv", "uv", "tool"),
    (4, 5, "Rf", "ruff", "tool"),
    (4, 6, "Pd", "Pydantic", "tool"),
    (4, 7, "Jp", "Jupyter", "tool"),
    (4, 8, "Vs", "VS Code", "tool"),
]

# ── career, drawn as a forest plot ────────────────────────────────────────
# (group, role, where, start "YYYY-MM", end "YYYY-MM" | None for ongoing)
GROUPS = {
    "industry": "orange",
    "research & teaching": "blue",
    "education": "aqua",
    "before data": "faint",
}

CAREER = [
    ("industry", "AI/ML Engineer", "Advance2000", "2025-11", None),
    ("industry", "AI Engineer", "NewLevelWork", "2025-01", "2025-11"),
    ("industry", "Data Scientist / ML Engineer", "NobleScripts", "2020-06", "2026-05"),
    (
        "industry",
        "Data Scientist / Statistician",
        "ClinStatDevice / ClinSoft",
        "2019-06",
        "2020-06",
    ),
    ("industry", "IT Intern · SQL, NLP", "Veon Armenia", "2018-09", "2018-11"),
    ("research & teaching", "Teaching Associate", "AUA", "2021-01", "2021-05"),
    ("research & teaching", "Research Assistant", "PDRF", "2020-07", "2021-03"),
    ("research & teaching", "EPIC Startup Program", "MetaStyle", "2020-01", "2020-06"),
    (
        "research & teaching",
        "AI Incubator",
        "Hero House · Expper",
        "2019-07",
        "2019-10",
    ),
    ("education", "Master, IE & Systems Mgmt", "AUA", "2017-09", "2020-06"),
    ("education", "Bachelor, Crisis Management", "ASUE", "2010-09", "2016-06"),
    (
        "before data",
        "Digitalization of Accounting",
        "Wikimedia Armenia",
        "2017-06",
        "2017-08",
    ),
    ("before data", "Accountant", "IT, retail & public", "2015-08", "2017-09"),
    ("before data", "Judicial Acts Specialist", "", "2014-03", "2015-08"),
    ("before data", "Military Service", "Armed Forces of RA", "2011-12", "2013-12"),
]
POOLED = ("pooled estimate", "data & ml", "2019-06")

# ── daily rotations ───────────────────────────────────────────────────────
QUOTES = [
    ("Essentially, all models are wrong, but some are useful.", "George E. P. Box"),
    (
        "The first principle is that you must not fool yourself — and you are the easiest person to fool.",
        "Richard Feynman",
    ),
    (
        "Nothing in biology makes sense except in the light of evolution.",
        "Theodosius Dobzhansky",
    ),
    ("We are a way for the cosmos to know itself.", "Carl Sagan"),
    ("The limits of my language mean the limits of my world.", "Ludwig Wittgenstein"),
    ("Whereof one cannot speak, thereof one must be silent.", "Ludwig Wittgenstein"),
    (
        "Mathematics is the art of giving the same name to different things.",
        "Henri Poincaré",
    ),
    ("What I cannot create, I do not understand.", "Richard Feynman"),
    (
        "The universe is not only queerer than we suppose, but queerer than we can suppose.",
        "J. B. S. Haldane",
    ),
    (
        (
            "Far better an approximate answer to the right question, which is often vague, "
            "than an exact answer to the wrong question, which can always be made precise."
        ),
        "John Tukey",
    ),
    ("The purpose of computing is insight, not numbers.", "Richard Hamming"),
    ("It is a capital mistake to theorize before one has data.", "Arthur Conan Doyle"),
    ("If you torture the data long enough, it will confess.", "Ronald Coase"),
    ("One must imagine Sisyphus happy.", "Albert Camus"),
    ("He who has a why to live can bear almost any how.", "Friedrich Nietzsche"),
    ("The map is not the territory.", "Alfred Korzybski"),
    ("The unexamined life is not worth living.", "Socrates"),
    (
        "If I have seen further it is by standing on the shoulders of Giants.",
        "Isaac Newton",
    ),
    (
        "The theory of probabilities is at bottom nothing but common sense reduced to calculus.",
        "Pierre-Simon Laplace",
    ),
    (
        "We are all in the gutter, but some of us are looking at the stars.",
        "Oscar Wilde",
    ),
    ("The Cosmos is all that is or ever was or ever will be.", "Carl Sagan"),
    (
        (
            "Nature uses only the longest threads to weave her patterns, so that each small piece "
            "of her fabric reveals the organization of the entire tapestry."
        ),
        "Richard Feynman",
    ),
    ("Everything flows.", "Heraclitus"),
    (
        (
            "Biology is the study of complicated things that give the appearance of having been designed for a purpose."
        ),
        "Richard Dawkins",
    ),
    (
        "Not everything that can be counted counts, and not everything that counts can be counted.",
        "William Bruce Cameron",
    ),
    (
        "The greatest value of a picture is when it forces us to notice what we never expected to see.",
        "John Tukey",
    ),
    (
        (
            "Two things fill the mind with ever new and increasing admiration and awe: "
            "the starry heavens above me and the moral law within me."
        ),
        "Immanuel Kant",
    ),
    (
        "The most beautiful thing we can experience is the mysterious.",
        "Albert Einstein",
    ),
    (
        (
            "Equipped with his five senses, man explores the universe around him and calls the adventure Science."
        ),
        "Edwin Hubble",
    ),
    ("My formula for greatness in a human being is amor fati.", "Friedrich Nietzsche"),
    ("I think, therefore I am.", "René Descartes"),
]

EQUATIONS = [
    ("P(θ|x) = P(x|θ) · P(θ) / P(x)", "bayes' theorem"),
    ("e^(iπ) + 1 = 0", "euler's identity"),
    ("iħ ∂ψ/∂t = Ĥψ", "schrödinger equation"),
    ("S = k · log W", "boltzmann entropy"),
    ("H(X) = −∑ p(x) log p(x)", "shannon entropy"),
    ("E = mc²", "mass–energy equivalence"),
    ("Gμν + Λgμν = (8πG/c⁴) Tμν", "einstein field equations"),
    ("∇ · E = ρ / ε₀", "gauss's law"),
    ("Δx · Δp ≥ ħ/2", "heisenberg uncertainty"),
    ("p² + 2pq + q² = 1", "hardy–weinberg equilibrium"),
    ("x[n+1] = r · x[n] · (1 − x[n])", "logistic map"),
    ("dx/dt = σ(y − x)", "lorenz system"),
    ("θ ← θ − η ∇L(θ)", "gradient descent"),
    ("softmax(QK⊤ / √d) V", "scaled dot-product attention"),
    ("v = Vmax [S] / (Km + [S])", "michaelis–menten kinetics"),
    ("H² = 8πGρ/3 − kc²/a² + Λc²/3", "friedmann equation"),
    ("v = H₀ d", "hubble–lemaître law"),
    ("F(ξ) = ∫ f(x) e^(−2πixξ) dx", "fourier transform"),
    ("dx/dt = αx − βxy", "lotka–volterra"),
    ("dS ≥ δQ / T", "second law of thermodynamics"),
    ("F = G m₁m₂ / r²", "newton's law of gravitation"),
    ("E = hν", "planck relation"),
    ("β = (X′X)⁻¹ X′y", "ordinary least squares"),
    ("φ = (1 + √5) / 2", "golden ratio · phyllotaxis"),
    ("D(P‖Q) = ∑ P(x) log P(x)/Q(x)", "kullback–leibler divergence"),
]


def of_the_day(items: list, today: date, salt: int = 0):
    """Deterministic daily pick; `salt` decorrelates rotations of equal length."""
    return items[(today.toordinal() * 7 + salt) % len(items)]
