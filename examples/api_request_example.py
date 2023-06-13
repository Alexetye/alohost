from alohost import AloHost
import asyncio
import os

TOKEN = os.getenv('API_TOKEN')

alo_host_session = AloHost(TOKEN, 'v3')
alo_host = alo_host_session.get_api()

async def main():
    
    all_projects = await alo_host.projects()
    frist_project_id = all_projects[0]['id']
    
    new_story = {'name': 'My new story', 'project_id': frist_project_id}
    story = await alo_host.stories.create(**new_story)
    print(story)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
