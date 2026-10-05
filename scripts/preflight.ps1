# Workshop preflight for Windows PowerShell:  powershell -ExecutionPolicy Bypass -File scripts\preflight.ps1
# Prints PASS/FAIL per check and the hostnames to hand to your network team if anything failed.
$McpUrl = if ($env:MCP_URL) { $env:MCP_URL } else { "https://d3m5dyfy6s31ka.cloudfront.net/mcp" }
$Base = $McpUrl -replace "/mcp$", ""
$Failed = @()
function Test-Reach($Name, $Url) {
  try {
    $r = Invoke-WebRequest -Uri $Url -Method Get -UseBasicParsing -TimeoutSec 15 -MaximumRedirection 0 -ErrorAction Stop
    Write-Host ("PASS  {0,-34} (HTTP {1})" -f $Name, $r.StatusCode)
  } catch {
    if ($_.Exception.Response) { Write-Host ("PASS  {0,-34} (HTTP {1})" -f $Name, [int]$_.Exception.Response.StatusCode) }
    else { Write-Host ("FAIL  {0,-34} no connection" -f $Name); $script:Failed += ([uri]$Url).Host }
  }
}
Write-Host "Workshop preflight - $(Get-Date -Format 'yyyy-MM-dd HH:mm')`n"
Test-Reach "CrewAI Studio (app.crewai.com)" "https://app.crewai.com/"
Test-Reach "PyPI index (pypi.org)"          "https://pypi.org/simple/crewai/"
Test-Reach "PyPI files"                      "https://files.pythonhosted.org/"
Test-Reach "GitHub"                          "https://github.com/"
Test-Reach "GitHub Codespaces"               "https://github.com/codespaces"
Test-Reach "OpenAI API"                      "https://api.openai.com/v1/models"
try {
  $h = Invoke-RestMethod -Uri "$Base/health" -TimeoutSec 15
  if ($h.status -eq "ok") { Write-Host "PASS  Workshop data connector (health)" } else { throw "bad" }
} catch { Write-Host "FAIL  Workshop data connector (health)"; $Failed += ([uri]$Base).Host }
$init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"preflight","version":"1"}}}'
try {
  $r = Invoke-WebRequest -Uri $McpUrl -Method Post -Body $init -ContentType "application/json" -Headers @{Accept="application/json, text/event-stream"} -UseBasicParsing -TimeoutSec 15
  if ($r.Content -match "northwind-workshop") { Write-Host "PASS  Workshop data connector (MCP handshake)" } else { throw "bad" }
} catch { Write-Host "FAIL  Workshop data connector (MCP handshake)" }
Write-Host ""
if ($Failed.Count -eq 0) { Write-Host "All network checks passed." }
else { Write-Host "Blocked from this network. Ask your network team to allow HTTPS (443) to:"; $Failed | Sort-Object -Unique | ForEach-Object { Write-Host "  $_" }; exit 1 }
