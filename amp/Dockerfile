# CrewAI workshop lab - dev container image
#
# Everything an attendee needs is baked in at build time: Python, uv, the CrewAI CLI and the
# lab project with its dependencies. No packages are installed when the container runs.
# Pinning: base images by digest; the dependencies by the labs' (identical) uv.lock files; the CrewAI CLI
# at its top-level version (crewai==1.15.23).
# Crews are never run locally in this container - they are deployed to CrewAI AMP and run there.
#
# Build:  docker buildx build --platform linux/amd64,linux/arm64 -t <registry>/crewai-workshop-lab:<tag> amp/
# Start:  docker run -d --name crewai-lab --restart unless-stopped <registry>/crewai-workshop-lab:<tag>

FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1

ARG REVISION=unknown
LABEL org.opencontainers.image.title="CrewAI workshop lab" \
      org.opencontainers.image.description="Dev container for the CrewAI workshop labs (Policy Q&A, Intake Triage, Renewal Prep, Bring Your Own)" \
      org.opencontainers.image.revision="${REVISION}"

# Optional, build time only: if your network re-signs HTTPS, put your root CA in amp/certs/
# as a .crt file so apt and git can fetch packages while building. The folder can stay empty.
# The CrewAI CLI does not use this store: app.crewai.com and login.crewai.com need direct
# access without TLS inspection.
COPY certs/ /usr/local/share/ca-certificates/
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates git curl nano less \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# uv, pinned, copied from its official image
COPY --from=ghcr.io/astral-sh/uv:0.11.19@sha256:b46b03ddfcfbf8f547af7e9eaefdf8a39c8cebcba7c98858d3162bd28cf536f6 /uv /uvx /usr/local/bin/

# Non-root user that owns the lab
RUN useradd --create-home --shell /bin/bash crew
USER crew
WORKDIR /home/crew

# ONE shared virtual environment serves the CrewAI CLI and all four labs (their uv.lock files pin
# the same packages; only the project name differs). Every lab's .venv is a symlink to it, so VS Code
# finds the interpreter, and UV_PROJECT_ENVIRONMENT points uv at it. UV_NO_SYNC stops `uv run`
# (used by `crewai deploy validate`) from re-installing the project into the shared environment,
# which would need the network. Crews are never run here, so this is all the container needs.
ENV VIRTUAL_ENV=/home/crew/.venv \
    UV_PROJECT_ENVIRONMENT=/home/crew/.venv \
    UV_NO_SYNC=1 \
    PATH=/home/crew/.local/bin:$PATH \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    CREWAI_DISABLE_TELEMETRY=true \
    OTEL_SDK_DISABLED=true

# Dependencies from the lock (crewai==1.15.23, which also provides the `crewai` CLI). The uv download
# cache lives in a build cache mount, so it is never stored in an image layer.
RUN --mount=type=cache,target=/home/crew/.cache/uv,uid=1000,gid=1000 \
    --mount=type=bind,source=lab/policy_qa/pyproject.toml,target=/tmp/proj/pyproject.toml \
    --mount=type=bind,source=lab/policy_qa/uv.lock,target=/tmp/proj/uv.lock \
    uv sync --project /tmp/proj --frozen --no-install-project --no-dev --python /usr/local/bin/python3 \
 && mkdir -p /home/crew/.local/bin \
 && ln -s /home/crew/.venv/bin/crewai /home/crew/.local/bin/crewai

# The lab projects, finished solutions, workshop tools and sample files for the BYO lab
COPY --chown=crew:crew lab/ /home/crew/lab/
COPY --chown=crew:crew solutions/ /home/crew/lab/solutions/
COPY --chown=crew:crew tools/ /home/crew/lab/tools/
COPY --chown=crew:crew byo-files/ /home/crew/lab/byo-files/

# Each lab is a git repo with a first commit (the CLI would otherwise create one on first deploy),
# an empty .env, and a .venv symlink to the shared environment. The symlink is git-ignored and the CLI's
# deploy zip skips both .venv and symlinks. `touch uv.lock` keeps the lock newer than pyproject.toml.
RUN git config --global user.name "CrewAI lab" \
 && git config --global user.email "lab@example.com" \
 && git config --global init.defaultBranch main \
 && for lab in policy_qa intake_triage renewal_prep bring_your_own; do \
      cd /home/crew/lab/$lab \
      && touch uv.lock \
      && printf '.venv\n__pycache__/\n*.pyc\n.env\n' > .gitignore \
      && git init -q && git add -A && git commit -qm "Lab starting point" \
      && printf '# Intentionally empty. On AMP, your deployment gets OPENAI_API_KEY from an organization variable you link to it.\n' > .env \
      && ln -s /home/crew/.venv .venv ; \
    done \
 && for lab in policy_qa intake_triage renewal_prep bring_your_own; do \
      cd /home/crew/lab/solutions/$lab \
      && touch uv.lock \
      && printf '# Intentionally empty. On AMP, your deployment gets OPENAI_API_KEY from an organization variable you link to it.\n' > .env \
      && ln -s /home/crew/.venv .venv ; \
    done

COPY --chown=crew:crew scripts/ /home/crew/scripts/
RUN cat /home/crew/scripts/bashrc-snippet >> /home/crew/.bashrc

WORKDIR /home/crew
CMD ["sleep", "infinity"]
