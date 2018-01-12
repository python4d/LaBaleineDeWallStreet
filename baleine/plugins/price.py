from baleine import command, exchange, util


class Price(command.Command):
    name = 'price'

    async def execute(self, message, args):
        if len(args) == 0:
            await self.error('il me faut un symbole')
            return

        symbol = args[0].upper()
        if len(symbol) > 3 and symbol.endswith(('BTC', 'XBT', 'ETH', 'USD', 'EUR')):
            tickers = (symbol[:-3], symbol[-3:])
        else:
            if symbol in ('BTC', 'XBT'):
                tickers = ('BTC', 'USD')
            else:
                tickers = (symbol, 'BTC')

        # Get exchange from pair or the one given on command
        if len(args) >= 2:
            try:
                xchg = exchange.get(args[1].lower())
            except KeyError:
                await self.error('je ne connais pas cet exchange.')
                return
        else:
            try:
                xchg = exchange.pair(tickers)
            except ValueError:
                await self.error('je ne connais pas ce coin.')
                return

        # Get prices
        try:
            prices = await xchg.get_prices(tickers)
        except IOError:
            await self.error('je n\'ai pas trouvé le prix sur cet exchange.')
            return

        await self.send(
            '{exchange} {tickers[0]}/{tickers[1]}: {last} [{change:+.2%}], {volume} vol'.format(
                exchange=xchg.name.capitalize(),
                tickers=tickers,
                last=util.format_price(prices.last, tickers[1], hide_ticker=True),
                change=prices.change,
                volume=util.format_price(prices.volume, tickers[0], hide_ticker=True),
            )
        )

