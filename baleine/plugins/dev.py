import asyncio
from baleine import command


class Id(command.Command):
    """ Bot command that tells the id of some discord objects, for debugging purposes """
    name = 'idof'

    errors = {
        'needs_server': 'only usable on a server',
        'usage': '{name} type name',
        'unknown_type': 'known types: {types}',
        'not_found': '{type} {name} not found',
    }

    async def execute(self, message, args):
        if message.server is None:
            await self.error('needs_server')
            return
        if len(args) != 2:
            await self.error('usage', name=self.name)
            return

        kind, name = args[0].lower(), args[1].lower()

        collections = {
            'channel': message.server.channels,
            'member': message.server.members,
            'role': message.server.roles,
        }
        items = collections.get(kind)

        if items is None:
            await self.error('unknown_type', types=', '.join(collections))
            return

        for item in items:
            if item.name.lower() == name:
                await self.send('{type} {name} has id {id}'.format(
                                type=kind, name=name, id=item.id))
                break
        else:
            await self.error('not_found', type=kind, name=name)
