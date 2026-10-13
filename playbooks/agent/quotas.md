---
topic: quotas
titleEn: Quotas and error codes
resourceUri: endleaf://guide/quotas
order: 7
---

# en

This key: plan {{plan}} ({{planStatus}}). Limits are the same numbers getQuota returns: `jobsPerDay` {{jobsPerDay}}, `perMinute` {{perMinute}}, `maxInputKiB` {{maxInputKiB}}. A job is one successful renderDocument. uploadSource and this guide do not spend a job. Playbook reads share `playbookReadsPerMinute` {{playbookReadsPerMinute}}. A failed or busy render does not spend a job. Fix the source and send it again. Do not loop.

`rejectBusy` is JSON-RPC HTTP 429 with `retryAfterSec` {{retryAfterSec}}. Wait, then send again.

## Error codes

- `rejectBadKey`: missing or rejected key. HTTP 401.
- `rejectKillSwitch`: rendering is stopped. HTTP 403.
- `rejectStoreDown`: keys cannot be read. HTTP 503.
- `rejectOverQuota`: this key is at its job cap. HTTP 429.
- `rejectPlaybookRate`: playbook reads over the per-minute limit. HTTP 429.
- `rejectInvalidInput`: the request is not usable. HTTP 400 or HTTP 200 with `isError`.
- `rejectPreflight`: refused construct. HTTP 200 with `isError`.
- `rejectBusy`: busy. JSON-RPC HTTP 429.
- `rejectUnreachable`: render service unreachable. HTTP 503.
- `rejectNoResult`: no result in time. HTTP 504.
- `failTimeout`: job ran too long. HTTP 504.
- `failCapHit`: resource cap. HTTP 502.
- `rejectSpawnFail`: job did not start. HTTP 502.
- `rejectLinkDropped`: connection dropped. HTTP 502.
- `rejectRenderError`: TeX failed. HTTP 200 with `isError`. Read `errorText`, fix, resend.
- `rejectUnboundConfig`: service not configured. HTTP 503.
