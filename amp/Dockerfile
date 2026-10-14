# CrewAI workshop lab - dev container image
#
# Everything an attendee needs is baked in at build time: Python, uv, the CrewAI CLI and the
# lab project with its dependencies. Nothing is downloaded when the container runs.
# Crews are never run locally in this container - they are deployed to CrewAI AMP and run there.
#
# Build:  docker buildx build --platform linux/amd64,linux/arm64 -t <registry>/crewai-workshop-lab:<tag> amp/
# Start:  docker run -d --name crewai-lab --restart unless-stopped <registry>/crewai-workshop-lab:<tag>

FROM python:3.12-slim

# Optional: if your network re-signs HTTPS (TLS inspection), put your root CA in
# amp/certs/ as a .crt file before building. The folder can stay empty otherwise.
COPY certs/ /usr/local/share/ca-certificates/
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates git curl nano less \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# uv, pinned, copied from its official image
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /usr/local/bin/

# Non-root user that owns the lab
RUN useradd --create-home --shell /bin/bash crew
USER crew
WORKDIR /home/crew
ENV PATH=/home/crew/.local/bin:$PATH \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    CREWAI_DISABLE_TELEMETRY=true \
    OTEL_SDK_DISABLED=true

# The CrewAI CLI, pinned to the workshop version
RUN uv tool install crewai==1.15.23

# The lab project, with its dependencies installed into lab/policy_qa/.venv
COPY --chown=crew:crew lab/ /home/crew/lab/
RUN cd /home/crew/lab/policy_qa \
 && uv sync --frozen --python /usr/local/bin/python3 \
 && touch uv.lock

# The CLI turns the project into a git repo on first deploy if it isn't one already;
# doing it here keeps that step out of the attendee's way.
RUN git config --global user.name "CrewAI lab" \
 && git config --global user.email "lab@example.com" \
 && git config --global init.defaultBranch main \
 && cd /home/crew/lab/policy_qa \
 && printf '.venv/\n__pycache__/\n*.pyc\n.env\n' > .gitignore \
 && git init -q && git add -A && git commit -qm "Lab starting point" \
 && printf '# Intentionally empty. The model key is set once for the whole AMP organization.\n' > .env

COPY --chown=crew:crew scripts/ /home/crew/scripts/
RUN cat /home/crew/scripts/bashrc-snippet >> /home/crew/.bashrc

WORKDIR /home/crew/lab/policy_qa
CMD ["sleep", "infinity"]
