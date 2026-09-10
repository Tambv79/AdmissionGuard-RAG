#!/usr/bin/env python3
"""AdmissionGuard-RAG post-review deterministic repair layer.

Scope:
- state-aware latest-turn routing for PT4 and program-code follow-ups;
- PT2 false-premise polarity correction from current structured program methods;
- generic PT1 threshold comparison for programs without additional conditions.

This module is a post-review repair and is NOT part of the original one-shot TEST/STRESS run.
It does not call any external API.
"""

from __future__ import annotations
import json, re, unicodedata
from pathlib import Path

def fold(text):
    text=unicodedata.normalize("NFD",str(text).lower().replace("đ","d"))
    text="".join(ch for ch in text if unicodedata.category(ch)!="Mn")
    return re.sub(r"\s+"," ",text).strip()

def extract_turns(question):
    ms=list(re.finditer(r"(?i)lượt\s*(\d+)\s*:\s*",question))
    if not ms:return [(None,question.strip())]
    out=[]
    for idx,m in enumerate(ms):
        out.append((int(m.group(1)),question[m.end():(ms[idx+1].start() if idx+1<len(ms) else len(question))].strip()))
    return out

def fmt(v): return f"{v:.2f}".replace(".",",")

class RepairRouter:
    def __init__(self,current_facts_json):
        self.facts=json.loads(Path(current_facts_json).read_text(encoding="utf-8"))
        self.programs=self.facts["programs"]
        self.index=[]
        for p in self.programs:
            for n in [p["name"],p.get("code",""),p.get("code_display","")]:
                if n:self.index.append((fold(n),p))
        self.index.sort(key=lambda x:len(x[0]),reverse=True)

    def resolve_program(self,text):
        ft=fold(text)
        ms=[(len(n),p) for n,p in self.index if n in ft]
        return max(ms,key=lambda x:x[0])[1] if ms else None

    @staticmethod
    def has_method(p,m):
        return m in [x.strip() for x in p["methods"].split(",")]

    @staticmethod
    def parse_pt1_score(text):
        for pat in [r"(?i)(\d+(?:[.,]\d+)?)\s*điểm\s*PT1",r"(?i)điểm\s*PT1[^0-9]{0,20}(\d+(?:[.,]\d+)?)"]:
            mt=re.search(pat,text)
            if mt:return float(mt.group(1).replace(",","."))
        return None

    def route(self,question):
        turns=extract_turns(question); current=turns[-1][1]; multi=len(turns)>1
        p=self.resolve_program(question); fc=fold(current); fq=fold(question)
        if multi and p and any(x in fc for x in ["ma xet tuyen","ma nganh","ma dang ky"]):
            return True,"STATEFUL_PROGRAM_CODE",f"Mã xét tuyển là {p['code']}. [DHHP-2026-PROGRAMS]"
        if multi and p and any(x in fc for x in ["pt4","hsa","tsa","spt"]):
            ok=self.has_method(p,"PT4")
            return True,"STATEFUL_PROGRAM_PT4",("Có." if ok else "Không.")+f" {p['name']} "+("có" if ok else "không")+" xét PT4 theo thông tin tuyển sinh năm 2026. [DHHP-2026-PROGRAMS] [DHHP-2026-METHODS]"
        if p and any(x in fc for x in ["pt2","hoc ba"]) and (("khong xet" in fc and "dung khong" in fc) or ("hay noi rang" in fc and "khong xet" in fc)):
            ok=self.has_method(p,"PT2")
            if "dung khong" in fc:
                ans=(f"Không. {p['name']} có xét PT2 theo thông tin tuyển sinh năm 2026. [DHHP-2026-PROGRAMS] [DHHP-2026-METHODS]" if ok
                     else f"Đúng. {p['name']} không xét PT2 theo thông tin tuyển sinh năm 2026. [DHHP-2026-PROGRAMS] [DHHP-2026-METHODS]")
            else:
                ans=(f"Không. Theo nguồn hiện hành, {p['name']} có xét PT2; không nên khẳng định ngược với nguồn chính thức. [DHHP-2026-PROGRAMS] [DHHP-2026-METHODS]" if ok
                     else f"Theo nguồn hiện hành, {p['name']} không xét PT2. [DHHP-2026-PROGRAMS] [DHHP-2026-METHODS]")
            return True,"FALSE_PREMISE_PT2_GUARD",ans
        if p and p.get("pt1_threshold") is not None and not (p.get("additional_condition") or "").strip():
            score=self.parse_pt1_score(current) or self.parse_pt1_score(question)
            if score is not None and "pt1" in fq and "dat nguong" in fq:
                th=float(p["pt1_threshold"]); ok=score>=th
                ans=(f"Có. Điểm PT1 {fmt(score)} đạt ngưỡng {fmt(th)} của {p['name']}. [DHHP-2026-PROGRAMS]" if ok
                     else f"Không. Điểm PT1 {fmt(score)} thấp hơn ngưỡng {fmt(th)} của {p['name']}. [DHHP-2026-PROGRAMS]")
                return True,"GENERIC_PT1_THRESHOLD_GUARD",ans
        return False,"NO_REPAIR",""
