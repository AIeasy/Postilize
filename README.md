<div align="center">

<h1>Postilize Instagram Message Sender</h1>

</div>

## What is PIMS?

**P**ostilize **I**nstagram **M**essage **S**ender is a tool utilizing agentQL and playwright api to help you send message via instagram

### Features

- **Manual login** Manually input your username and password and send the message!
- **Json login** Support Json login to save your hand and time!
- **Pop up handling** Program will handle all the popup so it won't stopping you!
- **Two_step handling** Program will ask you to input verification code when facing two-step checks!
- **Error Logging** Notice user errors with error code and reason!
- **Headless support** Program can excute all the action in silent!

## Quick Start

1. Install Python SDK and dependencies via your terminal:

```bash
pip install agentql
agentql init
```

2. Copy and paste [your API key](https://docs.agentql.com/dev) into the terminal.

3.Run the code with your choice of headless or not:

```bash
python UI.py head
```
OR
```bash
python UI.py headless
```

## Future work
There are some points I want to share:
- **AgentQL Hallucinations** Because of how AgentQL is made, sometime it will not locate the right element, this can be fixed by more fine-tunned prompting
- **Json encryption** To make sure there is not leaking of user's info, the Json file need to be encrypted, but I dont know what kind of encryption that Postilize is using so I leave it raw for now.
- **AgentQL's limitaion with Playwright** During the coding, I faced a problem that AgentQL is not able to locate the actual button elements, I reported this issue to the offical team and end-up helping them to find the right solution!

