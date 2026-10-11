import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  ArrowUpRight,
  Award,
  BarChart3,
  BriefcaseBusiness,
  Building2,
  Check,
  FileText,
  Gauge,
  Globe2,
  Layers3,
  Moon,
  Search,
  ShieldCheck,
  Sparkles,
  Sun,
  Target,
  UploadCloud,
  X,
  Zap
} from "lucide-react";

import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

const pages = [
  ["Overview", Gauge],
  ["Resume Health", Activity],
  ["ATS Audit", ShieldCheck],
  ["Job Match", Target],
  ["Content Coach", Sparkles],
  ["Company Intel", Building2],
  ["Interview Prep", BriefcaseBusiness]
];

function scoreColor(v) {
  return v >= 80 ? "good" : v >= 60 ? "warn" : "bad";
}


/* =========================================================
   APP
========================================================= */

function App() {
  const [dark, setDark] = useState(true);
  const [page, setPage] = useState("Overview");

  const [file, setFile] = useState(null);
  const [job, setJob] = useState("");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");

  const [analysis, setAnalysis] = useState(null);
  const [research, setResearch] = useState(null);

  const [loading, setLoading] = useState(false);
  const [researching, setResearching] = useState(false);

  const [error, setError] = useState("");

  /* =========================================================
     RESUME ANALYSIS
  ========================================================= */

  async function runAnalysis() {
    if (!file) {
      setError("Upload your resume first.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const form = new FormData();

      form.append("resume", file);
      form.append("job_description", job);
      form.append("company", company);
      form.append("role", role);

      const r = await fetch(`${API}/api/analyze`, {
        method: "POST",
        body: form
      });

      const data = await r.json();

      if (!r.ok) {
        throw new Error(data.detail || "Analysis failed");
      }

      setAnalysis(data);
      setPage("Overview");

    } catch (e) {
      setError(e.message || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  }


  /* =========================================================
     COMPANY RESEARCH
  ========================================================= */

  async function runResearch(companyName = company) {
    const targetCompany = companyName?.trim();

    if (!targetCompany) {
      return;
    }

    setResearch(null);
    setResearching(true);

    try {
      const r = await fetch(`${API}/api/research-company`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          company: targetCompany
        })
      });

      const data = await r.json();

      if (!r.ok) {
        throw new Error(
          data.detail || "Company research failed."
        );
      }

      console.log("Company research:", data);

      setResearch(data);

    } catch (e) {
      console.error("Company research error:", e);

      setResearch({
        company: targetCompany,
        source: "Error",
        answer: e.message || "Company research failed.",
        results: []
      });

    } finally {
      setResearching(false);
    }
  }


  /* =========================================================
     RADAR DATA
  ========================================================= */

  const s = analysis?.scores;

  const radar = useMemo(
    () =>
      s
        ? [
            {
              subject: "ATS",
              value: s.ats
            },
            {
              subject: "Skills",
              value: s.skill_match
            },
            {
              subject: "Keywords",
              value: s.keywords
            },
            {
              subject: "Semantic",
              value: s.semantic_match
            },
            {
              subject: "Evidence",
              value: s.evidence
            },
            {
              subject: "Interview",
              value: s.interview_readiness
            }
          ]
        : [],
    [s]
  );


  /* =========================================================
     MAIN UI
  ========================================================= */

  return (
    <div className={dark ? "app dark" : "app"}>

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brandMark">
            ✦
          </div>

          <div>
            <b>Resume Intelligence</b>
            <span>Career analytics platform</span>
          </div>

        </div>


        <div className="navLabel">
          WORKSPACE
        </div>


        {pages.map(([name, Icon]) => (
          <button
            key={name}
            className={
              page === name
                ? "nav active"
                : "nav"
            }
            onClick={() => setPage(name)}
          >
            <Icon size={17} />

            <span>{name}</span>

            {analysis && name === "Overview" && (
              <span className="dot" />
            )}
          </button>
        ))}


        <div className="sidebarBottom">

          <button
            className="themeBtn"
            onClick={() => setDark(!dark)}
          >
            {dark ? (
              <Sun size={17} />
            ) : (
              <Moon size={17} />
            )}

            {dark ? "Light mode" : "Dark mode"}
          </button>


          <div className="privacy">

            <ShieldCheck size={16} />

            <span>
              Session-first processing
              <br />
              Credentials stay server-side.
            </span>

          </div>

        </div>

      </aside>


      {/* MAIN */}

      <main>

        {/* TOP BAR */}

        <header className="topbar">

          <div>

            <span className="crumb">
              RESUME INTELLIGENCE
            </span>

            <span className="slash">
              /
            </span>

            <b>{page}</b>

          </div>


          <div className="topActions">

            <span className="status">
              <i />
              Engine ready
            </span>

            <button
              className="iconBtn"
              onClick={() => setDark(!dark)}
            >
              {dark ? (
                <Sun size={18} />
              ) : (
                <Moon size={18} />
              )}
            </button>

          </div>

        </header>


        {/* BEFORE ANALYSIS */}

        {!analysis ? (

          <UploadScreen
            file={file}
            setFile={setFile}
            job={job}
            setJob={setJob}
            company={company}
            setCompany={setCompany}
            role={role}
            setRole={setRole}
            runAnalysis={runAnalysis}
            loading={loading}
            error={error}
          />

        ) : (

          /* AFTER ANALYSIS */

          <div className="content">

            <div className="pageHead">

              <div>

                <span className="eyebrow">
                  ANALYSIS COMPLETE
                </span>

                <h1>
                  Resume intelligence
                </h1>

                <p>
                  {analysis.filename}
                  {" · "}
                  {analysis.company || "No company selected"}
                  {" · "}
                  evidence-based analysis
                </p>

              </div>


              <button
                className="secondary"
                onClick={() => {
                  setAnalysis(null);
                  setResearch(null);
                  setError("");
                }}
              >
                <UploadCloud size={16} />

                Analyze another resume
              </button>

            </div>


            {page === "Overview" && (
              <Overview
                analysis={analysis}
                radar={radar}
              />
            )}

            {page === "Resume Health" && (
              <Health analysis={analysis} />
            )}

            {page === "ATS Audit" && (
              <ATS analysis={analysis} />
            )}

            {page === "Job Match" && (
              <JobMatch analysis={analysis} />
            )}

            {page === "Content Coach" && (
              <Coach analysis={analysis} />
            )}

            {page === "Company Intel" && (
              <CompanyIntel
                analysis={analysis}
                company={company}
                setCompany={setCompany}
                research={research}
                onResearch={runResearch}
                researching={researching}
              />
            )}

            {page === "Interview Prep" && (
              <Interview analysis={analysis} />
            )}

          </div>
        )}

      </main>

    </div>
  );
}


/* =========================================================
   UPLOAD SCREEN
========================================================= */

function UploadScreen(p) {

  return (
    <div className="uploadPage">

      <section className="hero">

        <div className="eyebrow">
          AI-POWERED CAREER ANALYTICS
        </div>

        <h1>
          Turn your resume into a
          <br />
          <em>data-driven advantage.</em>
        </h1>

        <p>
          Go beyond a single score. Understand ATS readiness,
          role fit, keyword coverage, content quality and
          interview readiness — all in one workspace.
        </p>


        <div className="heroStats">

          <span>
            <Sparkles />
            AI reasoning
          </span>

          <span>
            <BarChart3 />
            Visual analytics
          </span>

          <span>
            <Globe2 />
            Company intelligence
          </span>

        </div>

      </section>


      <div className="setupGrid">

        {/* RESUME */}

        <section className="panel">

          <div className="panelTitle">

            <span className="step">
              01
            </span>

            <div>
              <b>Upload your resume</b>
              <small>
                PDF, DOCX or TXT · max 8 MB
              </small>
            </div>

          </div>


          <label className="drop">

            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={(e) =>
                p.setFile(
                  e.target.files?.[0] || null
                )
              }
            />

            <UploadCloud size={30} />

            <b>
              {p.file
                ? p.file.name
                : "Drop your resume here"}
            </b>

            <span>
              {p.file
                ? "Ready for analysis"
                : "or click to browse"}
            </span>

          </label>

        </section>


        {/* TARGET ROLE */}

        <section className="panel">

          <div className="panelTitle">

            <span className="step">
              02
            </span>

            <div>

              <b>Target role</b>

              <small>
                Optional, but recommended for job matching
              </small>

            </div>

          </div>


          <input
            className="input"
            value={p.role}
            onChange={(e) =>
              p.setRole(e.target.value)
            }
            placeholder="e.g. Data Analyst Intern"
          />


          <input
            className="input"
            value={p.company}
            onChange={(e) =>
              p.setCompany(e.target.value)
            }
            placeholder="Company (optional)"
          />


          <textarea
            className="textarea"
            value={p.job}
            onChange={(e) =>
              p.setJob(e.target.value)
            }
            placeholder="Paste the full job description here..."
          />

        </section>

      </div>


      {p.error && (
        <div className="error">
          {p.error}
        </div>
      )}


      <button
        className="primary analyzeBtn"
        onClick={p.runAnalysis}
        disabled={p.loading}
      >

        {p.loading ? (
          <>
            <span className="spinner" />
            Analyzing resume...
          </>
        ) : (
          <>
            Run full analysis
            <ArrowUpRight size={18} />
          </>
        )}

      </button>

    </div>
  );
}


/* =========================================================
   METRIC CARD
========================================================= */

function MetricCard({
  label,
  value,
  sub
}) {

  return (
    <div className="metricCard">

      <span>{label}</span>

      <strong
        className={scoreColor(value)}
      >
        {Math.round(value)}
      </strong>

      <small>{sub}</small>

    </div>
  );
}


/* =========================================================
   OVERVIEW
========================================================= */

function Overview({
  analysis: a,
  radar
}) {

  const s = a.scores;
  const ai = a.ai || {};

  return (
    <div className="stack">

      <div className="metrics">

        {[
          [
            "Overall score",
            s.overall,
            "/100"
          ],
          [
            "ATS readiness",
            s.ats,
            "document health"
          ],
          [
            "Skill match",
            s.skill_match,
            "target role"
          ],
          [
            "Keyword signal",
            s.keywords,
            "JD coverage"
          ],
          [
            "Interview readiness",
            s.interview_readiness,
            "prep signal"
          ]
        ].map((x) => (
          <MetricCard
            key={x[0]}
            label={x[0]}
            value={x[1]}
            sub={x[2]}
          />
        ))}

      </div>


      <div className="twoCol">

        {/* RADAR */}

        <section className="panel chartPanel">

          <div className="sectionHead">

            <div>

              <b>Resume profile</b>

              <small>
                Multi-dimensional view of application strength
              </small>

            </div>

            <span className="tag">
              <Activity size={14} />
              LIVE
            </span>

          </div>


          <div className="radarWrap">

            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <RadarChart data={radar}>

                <PolarGrid />

                <PolarAngleAxis
                  dataKey="subject"
                />

                <Radar
                  dataKey="value"
                  fill="rgba(139,124,255,.28)"
                  stroke="#8b7cff"
                  strokeWidth={2}
                  fillOpacity={1}
                />

                <Tooltip />

              </RadarChart>

            </ResponsiveContainer>

          </div>

        </section>


        {/* AI ASSESSMENT */}

        <section className="panel">

          <div className="sectionHead">

            <div>

              <b>
                Executive assessment
              </b>

              <small>
                AI recruiter perspective
              </small>

            </div>

            <Sparkles size={18} />

          </div>


          <p className="lead">

            {ai.executive_summary ||
              "AI commentary is currently unavailable. Your deterministic resume analysis is still available across the dashboard."}

          </p>


          <div className="insightList">

            {(ai.strengths || [])
              .slice(0, 4)
              .map((x, i) => (

                <div
                  className="insight"
                  key={i}
                >

                  <Check size={16} />

                  <span>{x}</span>

                </div>

              ))}

          </div>


          <div className="fitBox">

            <span>
              ROLE FIT
            </span>

            <b>
              {ai.role_fit ||
                "Based on deterministic job/resume evidence."}
            </b>

          </div>

        </section>

      </div>


      <div className="threeCol">

        <Mini
          title="Resume footprint"
          icon={<FileText />}
          items={[
            `${a.profile.word_count} words`,
            `${a.profile.sections_found} sections detected`,
            `${a.profile.quantified_achievements} quantified achievements`
          ]}
        />

        <Mini
          title="NLP pipeline"
          icon={<Layers3 />}
          items={[
            ...((a.nlp?.engines || []).map((engine) => `${engine} active`)),
            "TF-IDF similarity active",
            `${a.profile.nlp_entities || 0} entities detected`
          ]}
        />


        <Mini
          title="Contact readiness"
          icon={<Globe2 />}
          items={Object.entries(
            a.contact || {}
          ).map(
            ([k, v]) =>
              `${v ? "✓" : "○"} ${k.replaceAll(
                "_",
                " "
              )}`
          )}
        />


        <Mini
          title="Top priority"
          icon={<Zap />}
          items={(ai.rewrite_priorities || [])
            .slice(0, 3)}
        />

      </div>

    </div>
  );
}


/* =========================================================
   MINI CARD
========================================================= */

function Mini({
  title,
  icon,
  items
}) {

  return (
    <section className="panel mini">

      <div className="miniTitle">
        {icon}
        <b>{title}</b>
      </div>

      {items.map((x, i) => (
        <div
          className="miniRow"
          key={i}
        >
          {x}
        </div>
      ))}

    </section>
  );
}


/* =========================================================
   RESUME HEALTH
========================================================= */

function Health({ analysis: a }) {

  const d = a.writing;

  const chart = [
    ["ATS", a.scores.ats],
    ["Evidence", a.scores.evidence],
    ["Keywords", a.scores.keywords],
    ["Semantic", a.scores.semantic_match]
  ].map(
    ([name, value]) => ({
      name,
      value
    })
  );


  return (
    <div className="stack">

      <div className="sectionIntro">

        <h2>
          Resume health
        </h2>

        <p>
          A detailed view of the document itself,
          independent of a particular job.
        </p>

      </div>


      <div className="twoCol">

        <section className="panel">

          <div className="sectionHead">

            <b>
              Health distribution
            </b>

            <BarChart3 size={18} />

          </div>


          <ResponsiveContainer
            width="100%"
            height={310}
          >

            <BarChart
              data={chart}
              layout="vertical"
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                type="number"
                domain={[0, 100]}
              />

              <YAxis
                dataKey="name"
                type="category"
              />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#8b7cff"
                radius={[
                  0,
                  8,
                  8,
                  0
                ]}
              />

            </BarChart>

          </ResponsiveContainer>

        </section>


        <section className="panel">

          <div className="sectionHead">

            <b>
              Document statistics
            </b>

            <Layers3 size={18} />

          </div>


          <div className="statsGrid">

            {Object.entries(
              d || {}
            ).map(([k, v]) => (

              <div
                className="stat"
                key={k}
              >

                <small>
                  {k.replaceAll(
                    "_",
                    " "
                  )}
                </small>

                <b>{v}</b>

              </div>

            ))}

          </div>


          <h3>
            Detected sections
          </h3>


          <div className="chips">

            {Object.keys(
              a.sections || {}
            ).map((x) => (

              <span key={x}>
                {x}
              </span>

            ))}

          </div>

        </section>

      </div>

    </div>
  );
}


/* =========================================================
   ATS
========================================================= */

function ATS({ analysis: a }) {

  const risks = a.ats?.risks || [];

  return (
    <div className="stack">

      <div className="sectionIntro">

        <h2>
          ATS audit
        </h2>

        <p>
          Technical document checks designed to surface
          parser and screening risks — not a claim about
          any one vendor's proprietary score.
        </p>

      </div>


      <div className="threeCol">

        {[
          [
            "Structure",
            a.ats.structure_score,
            "standard headings"
          ],
          [
            "Contact",
            a.ats.contact_score,
            "reachability"
          ],
          [
            "Scanability",
            a.ats.scanability_score,
            "readability"
          ]
        ].map((x) => (

          <div
            className="panel gaugeCard"
            key={x[0]}
          >

            <GaugeRing
              value={x[1]}
            />

            <b>{x[0]}</b>

            <small>{x[2]}</small>

          </div>

        ))}

      </div>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Issues to resolve
          </b>

          <span className="count">
            {risks.length}
          </span>

        </div>


        {risks.length ? (

          risks.map((r, i) => (

            <div
              className={`risk ${r.severity}`}
              key={i}
            >

              <span>
                {String(
                  r.severity || "info"
                ).toUpperCase()}
              </span>

              <p>
                {r.message}
              </p>

            </div>

          ))

        ) : (

          <div className="success">

            <Check />

            No major deterministic ATS risks detected.

          </div>

        )}

      </section>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Quantified evidence
          </b>

          <Award size={18} />

        </div>


        {a.achievements?.length ? (

          a.achievements.map(
            (x, i) => (

              <div
                className="evidence"
                key={i}
              >

                <span>
                  {String(
                    i + 1
                  ).padStart(2, "0")}
                </span>

                <p>{x}</p>

              </div>

            )
          )

        ) : (

          <div className="empty">

            No measurable outcomes detected.
            Add truthful metrics to high-value bullets.

          </div>

        )}

      </section>

    </div>
  );
}


/* =========================================================
   GAUGE
========================================================= */

function GaugeRing({ value = 0 }) {

  return (
    <div
      className="ring"
      style={{
        "--value": `${value * 3.6}deg`
      }}
    >

      <div>

        <b>
          {Math.round(value)}
        </b>

        <small>
          /100
        </small>

      </div>

    </div>
  );
}


/* =========================================================
   JOB MATCH
========================================================= */

function JobMatch({ analysis: a }) {

  const [
    showMissing,
    setShowMissing
  ] = useState(true);

  const groups = showMissing
    ? a.skills.missing
    : a.skills.matched;


  return (
    <div className="stack">

      <div className="sectionIntro">

        <h2>
          Job match
        </h2>

        <p>
          Every requirement is traceable to
          the supplied job description.
        </p>

      </div>


      <div className="matchHero">

        <div>

          <span className="eyebrow">
            TARGET ROLE FIT
          </span>

          <strong>
            {Math.round(
              a.scores.skill_match
            )}
            %
          </strong>

          <p>
            {a.skills.matched.length}
            {" of "}
            {a.skills.all_job_terms.length}
            {" extracted job terms are evidenced."}
          </p>

        </div>


        <div className="matchBar">

          <span
            style={{
              width: `${a.scores.skill_match}%`
            }}
          />

        </div>

      </div>


      <div className="panel">

        <div className="toggleTabs">

          <button
            className={
              !showMissing
                ? "selected"
                : ""
            }
            onClick={() =>
              setShowMissing(false)
            }
          >
            Matched
            <b>
              {a.skills.matched.length}
            </b>
          </button>


          <button
            className={
              showMissing
                ? "selected"
                : ""
            }
            onClick={() =>
              setShowMissing(true)
            }
          >
            Needs evidence
            <b>
              {a.skills.missing.length}
            </b>
          </button>

        </div>


        <div className="termGrid">

          {groups.map((x) => (

            <div
              className="term"
              key={x}
            >

              <span>
                {showMissing ? (
                  <X />
                ) : (
                  <Check />
                )}
              </span>

              {x}

            </div>

          ))}

        </div>

      </div>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Keyword coverage
          </b>

          <span>
            {Math.round(
              a.scores.keywords
            )}
            %
          </span>

        </div>


        <div className="progress">

          <span
            style={{
              width: `${a.scores.keywords}%`
            }}
          />

        </div>


        <div className="chips">

          {a.keywords.matched
            .slice(0, 25)
            .map((x) => (

              <span key={x}>
                {x}
              </span>

            ))}

        </div>

      </section>

    </div>
  );
}


/* =========================================================
   CONTENT COACH
========================================================= */

function Coach({ analysis: a }) {

  const ai = a.ai || {};

  const rewritePriorities =
    ai.rewrite_priorities || [];

  const achievementUpgrades =
    ai.achievement_upgrades || [];

  const strengths =
    ai.strengths || [];

  const weaknesses =
    ai.weaknesses || [];


  return (
    <div className="stack">

      <div className="sectionIntro">

        <h2>
          Content coach
        </h2>

        <p>
          Prioritize truthful, evidence-backed
          changes instead of stuffing keywords
          into the resume.
        </p>

      </div>


      <div className="twoCol">

        <section className="panel">

          <div className="sectionHead">

            <b>
              Rewrite priorities
            </b>

            <Sparkles size={18} />

          </div>


          {rewritePriorities.length ? (

            rewritePriorities.map(
              (x, i) => (

                <div
                  className="numbered"
                  key={i}
                >

                  <span>
                    {String(
                      i + 1
                    ).padStart(2, "0")}
                  </span>

                  <p>{x}</p>

                </div>

              )
            )

          ) : (

            <div className="empty">

              Configure Hugging Face AI
              for detailed rewriting guidance.

            </div>

          )}

        </section>


        <section className="panel">

          <div className="sectionHead">

            <b>
              Achievement upgrades
            </b>

            <Award size={18} />

          </div>


          {achievementUpgrades.length ? (

            achievementUpgrades.map(
              (x, i) => (

                <div
                  className="upgrade"
                  key={i}
                >

                  <ArrowUpRight />

                  <p>{x}</p>

                </div>

              )
            )

          ) : (

            <div className="empty">

              No AI upgrade examples available.

            </div>

          )}

        </section>

      </div>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Strengths & weaknesses
          </b>

        </div>


        <div className="twoInner">

          <div>

            <h3>
              Strengths
            </h3>

            {strengths.map((x) => (

              <div
                className="bullet goodBullet"
                key={x}
              >

                <Check />

                {x}

              </div>

            ))}

          </div>


          <div>

            <h3>
              Weaknesses
            </h3>

            {weaknesses.map(
              (x, i) => (

                <div
                  className="bullet badBullet"
                  key={i}
                >

                  <X />

                  {x}

                </div>

              )
            )}

          </div>

        </div>

      </section>

    </div>
  );
}


/* =========================================================
   COMPANY INTELLIGENCE
========================================================= */

function CompanyIntel({
  analysis,
  company,
  setCompany,
  research,
  onResearch,
  researching
}) {

  return (
    <div className="stack">

      {/* INTRO */}

      <div className="sectionIntro">

        <h2>
          Company intelligence
        </h2>

        <p>
          Use current public-web information to
          turn generic preparation into
          company-specific preparation.
        </p>

      </div>


      {/* SEARCH */}

      <div className="researchBar">

        <Building2 size={20} />


        <input
          value={company}
          onChange={(e) =>
            setCompany(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              onResearch(company);
            }
          }}
          placeholder="Enter company name"
        />


        <button
          className="primary"
          onClick={() =>
            onResearch(company)
          }
          disabled={
            researching ||
            !company.trim()
          }
        >

          {researching ? (
            <>
              <span className="spinner" />
              Researching...
            </>
          ) : (
            <>
              <Search size={16} />
              Research
            </>
          )}

        </button>

      </div>


      {/* RESEARCH RESULTS */}

      {research && (

        <section className="panel">

          <div className="sectionHead">

            <div>

              <b>
                {research.company}
              </b>

              <small>
                Source:{" "}
                {research.source ||
                  "Public web research"}
              </small>

            </div>

            <Globe2 size={18} />

          </div>


          {/* SUMMARY */}

          {research.answer && (

            <div className="researchSummary">

              <div className="researchSummaryIcon">
                <Sparkles size={17} />
              </div>

              <div>

                <span className="eyebrow">
                  RESEARCH SUMMARY
                </span>

                <p className="lead">
                  {research.answer}
                </p>

              </div>

            </div>

          )}


          {/* SOURCES */}

          {research.results?.length > 0 && (

            <>

              <div className="sectionHead researchResultsHead">

                <div>

                  <b>
                    Relevant sources
                  </b>

                  <small>
                    Current public-web information
                    used for company research
                  </small>

                </div>

                <span className="count">
                  {research.results.length}
                </span>

              </div>


              <div className="results">

                {research.results.map(
                  (item, index) => (

                    <a
                      className="result"
                      href={item.url}
                      target="_blank"
                      rel="noreferrer"
                      key={index}
                    >

                      <div>

                        <b>
                          {item.title}
                        </b>


                        {item.snippet && (
                          <p>
                            {item.snippet}
                          </p>
                        )}


                        <small className="resultUrl">
                          {item.url}
                        </small>

                      </div>


                      <ArrowUpRight size={17} />

                    </a>

                  )
                )}

              </div>

            </>

          )}

        </section>

      )}


      {/* EMPTY STATE */}

      {!research && (

        <section className="panel researchEmpty">

          <div className="emptyIcon">

            <Globe2 size={28} />

          </div>


          <h3>
            Research a target company
          </h3>


          <p>
            Enter a company above to discover
            current hiring signals, culture
            information, interview insights,
            career pages and other useful
            public sources.
          </p>


          {analysis?.company && (

            <button
              className="secondary"
              onClick={() => {
                setCompany(
                  analysis.company
                );

                onResearch(
                  analysis.company
                );
              }}
            >

              <Building2 size={16} />

              Research {analysis.company}

            </button>

          )}

        </section>

      )}


      {/* ROLE CONTEXT */}

      <section className="panel">

        <div className="sectionHead">

          <div>

            <b>
              Role context
            </b>

            <small>
              How your resume aligns with
              the selected target
            </small>

          </div>

          <BriefcaseBusiness size={18} />

        </div>


        <div className="fitBox">

          <span>
            ROLE FIT
          </span>

          <b>
            {analysis?.ai?.role_fit ||
              "Run AI analysis with a target role for a tailored fit assessment."}
          </b>

        </div>

      </section>

    </div>
  );
}


/* =========================================================
   INTERVIEW PREP
========================================================= */

function Interview({ analysis: a }) {

  const ai = a.ai || {};

  const interviewTopics =
    ai.interview_topics || [];

  const interviewQuestions =
    ai.interview_questions || [];

  const prepPlan =
    ai.prep_plan || [];


  return (
    <div className="stack">

      <div className="sectionIntro">

        <h2>
          Interview prep
        </h2>

        <p>
          Questions and preparation topics
          generated from your resume and
          target role.
        </p>

      </div>


      <div className="prepGrid">

        <div className="prepScore">

          <span>
            INTERVIEW READINESS
          </span>

          <strong>
            {Math.round(
              a.scores.interview_readiness
            )}
          </strong>

          <small>
            / 100
          </small>

        </div>


        {ai.seniority_alignment && (

          <div className="panel">

            <div className="sectionHead">

              <b>
                Seniority alignment
              </b>

              <Target />

            </div>

            <p className="lead">
              {ai.seniority_alignment}
            </p>

          </div>

        )}

      </div>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Likely interview topics
          </b>

          <Search size={18} />

        </div>


        <div className="termGrid">

          {interviewTopics.map(
            (x, i) => (

              <div
                className="term"
                key={i}
              >

                <Target />

                {x}

              </div>

            )
          )}

        </div>

      </section>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Practice questions
          </b>

          <BriefcaseBusiness size={18} />

        </div>


        {interviewQuestions.map(
          (x, i) => (

            <div
              className="question"
              key={i}
            >

              <span>
                {String(
                  i + 1
                ).padStart(2, "0")}
              </span>

              <b>{x}</b>

            </div>

          )
        )}

      </section>


      <section className="panel">

        <div className="sectionHead">

          <b>
            Preparation plan
          </b>

          <Zap size={18} />

        </div>


        {prepPlan.map(
          (x, i) => (

            <div
              className="numbered"
              key={i}
            >

              <span>
                {i + 1}
              </span>

              <p>{x}</p>

            </div>

          )
        )}

      </section>

    </div>
  );
}


/* =========================================================
   APP START
========================================================= */

function AppError() {
  return null;
}

function MiniUnused() {}

function render() {
  createRoot(
    document.getElementById("root")
  ).render(
    <App />
  );
}

render();