from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ProgrammingLanguage(str, Enum):
    C = "C"
    CLOJURE = "Clojure"
    COFFEESCRIPT = "CoffeeScript"
    CPP = "C++"
    CRYSTAL = "Crystal"
    CSHARP = "C#"
    CSS = "CSS"
    D = "D"
    DART = "Dart"
    ELIXIR = "Elixir"
    ERLANG = "Erlang"
    FSHARP = "F#"
    FORTRAN = "Fortran"
    GO = "Go"
    GROOVY = "Groovy"
    HASKELL = "Haskell"
    HTML = "HTML"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"
    JSON = "JSON"
    JULIA = "Julia"
    KOTLIN = "Kotlin"
    LUA = "Lua"
    MARKDOWN = "Markdown"
    MATLAB = "MATLAB"
    NIM = "Nim"
    OBJECTIVE_C = "Objective-C"
    PERL = "Perl"
    PHP = "PHP"
    POWERSHELL = "PowerShell"
    PYTHON = "Python"
    R_LANG = "R"
    RACKET = "Racket"
    RUBY = "Ruby"
    RUST = "Rust"
    SCALA = "Scala"
    SCSS = "SCSS"
    SHELL = "Shell"
    SQL = "SQL"
    SWIFT = "Swift"
    TCL = "Tcl"
    TYPESCRIPT = "TypeScript"
    VB = "Visual Basic"
    VERILOG = "Verilog"
    VHDL = "VHDL"
    YAML = "YAML"
    ZIG = "Zig"
    UNKNOWN = "Unknown"


class License(str, Enum):
    AGPL_3_0 = "GNU Affero General Public License v3.0"
    APACHE_2_0 = "Apache License 2.0"
    ARTISTIC_2_0 = "Artistic License 2.0"
    BSD_2 = "BSD 2-Clause Simplified License"
    BSD_3 = "BSD 3-Clause New or Revised License"
    CC0_1_0 = "Creative Commons Zero v1.0 Universal"
    CC_BY_4_0 = "Creative Commons Attribution 4.0 International"
    CC_BY_SA_4_0 = "Creative Commons Attribution Share Alike 4.0 International"
    EPL_2_0 = "Eclipse Public License 2.0"
    GPL_2_0 = "GNU General Public License v2.0"
    GPL_3_0 = "GNU General Public License v3.0"
    ISC = "ISC License"
    LGPL_2_1 = "GNU Lesser General Public License v2.1"
    LGPL_3_0 = "GNU Lesser General Public License v3.0"
    MIT = "MIT License"
    MPL_2_0 = "Mozilla Public License 2.0"
    OSL_3_0 = "Open Software License 3.0"
    PROPRIETARY = "Proprietary"
    UNLICENSE = "The Unlicense"
    WTFPL = "Do What The F*ck You Want To Public License"
    ZLIB = "zlib License"
    UNKNOWN = "Unknown"


class StructuredOutput(BaseModel):
    description: str
    programming_language: ProgrammingLanguage
    license: License


def system_prompt() -> str:
    return """You are a data extraction assistant for a GitHub project metadata database.
For each GitHub repository, your job is to extract **three fields only**:

- description — a concise but informative summary of the project, at most 300 words, written in neutral and factual language.
  - Summarize what the project does, its main purpose, and what technologies or domains it involves.
  - Do NOT include installation instructions, badges, or code snippets.
  - If the description is missing or unclear, infer one from README context.
- programming_language — the repository's primary programming language, matching the ProgrammingLanguage enum (e.g. "Python", "JavaScript", "Go", "Rust", "Unknown").
- license — the repository's software license, matching the License enum (e.g. "MIT License", "Apache License 2.0", "GNU General Public License v3.0", "Unknown").

Output format:
Return results as strict JSON:
{
  "description": "",
  "programming_language": "",
  "license": ""
}

Rules:
- Do not exceed 300 words for the description.
- Do not include Markdown, HTML, emojis, or special characters.
- Do not generate fictional or speculative text — only summarize from repository content.
- If you cannot determine the programming language or license, return "Unknown".

Example:
{
  "description": "FastAPI is a modern web framework for building high-performance APIs in Python using standard type hints. It features automatic interactive documentation and support for asynchronous programming.",
  "programming_language": "Python",
  "license": "MIT License"
}
"""
