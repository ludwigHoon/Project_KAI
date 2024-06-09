# Vector DB schema

# Fatigue model
- temporary: 
    - trpakov/vit-face-expression
    - LLaVA (or similar multimodal) positive / negative

# Other integrations
1. ActivityWatch for productivity, use the data they provide instead of https://activitywatch.net/
2. Thunderbird, maybe use this: https://wiki.bitplan.com/index.php/PyThunderbird instead of outlook, since only the old outlook (which is not free anyhow) has COM API exposed, https://kb.mozillazine.org/Files_and_folders_in_the_profile_-_Thunderbird (for reading) pythunderbird 
    - found Google gmail and calander API is easily accessible. Use Google instead

```markdown
# Email title: 
# Email body:
....
```
- recipients (to, cc, bcc) --- metadata

```markdown
# Event name:
# Note:
```
- start time, end time, location, attendees --- metadata
- **Done** in Google Calender, see google_module.py, uncomment sample usage and run


## Demo(s) 
- Using only CPU
- Using "NPU"- 10-15s "NPU" performance (kiss ass time)

Without prompting:
- productivity suggestions (Activity watcher ....)
- email catch-up / follow-up? (background - cron tasks)
- Daily events
---How ? "schtasks /create /tn calculate /tr calc /sc weekly /d MON /st 06:05 /ru "System""

User prompting
- "What is my day like" 
- Helping with "research" <-- another kiss ass time <- AMD (download some AMD documentation (ASK about documents workflow))
