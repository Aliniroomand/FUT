"""
Unit tests for BUY flow handlers using mock backend_client and futbin.
Run: python -m unittest tests/test_buy_flow.py
"""
import unittest
from unittest.mock import AsyncMock, patch
from bot.handlers import buy

class BuyFlowTests(unittest.IsolatedAsyncioTestCase):
    @patch('bot.services.backend_client.get_transaction_status', new_callable=AsyncMock)
    @patch('bot.utils.rate_limiter.rate_limiter.is_allowed', return_value=True)
    async def test_start_buy_enabled(self, mock_rate, mock_status):
        mock_status.return_value = {'buying_disabled': False}
        update = AsyncMock()
        context = {'user_data': {}}
        await buy.start_buy(update, context)
        update.message.reply_text.assert_called()
        self.assertIn('buy_flow', context['user_data'])

    @patch('bot.services.backend_client.get_transaction_status', new_callable=AsyncMock)
    @patch('bot.utils.rate_limiter.rate_limiter.is_allowed', return_value=False)
    async def test_start_buy_rate_limited(self, mock_rate, mock_status):
        mock_status.return_value = {'buying_disabled': False}
        update = AsyncMock()
        context = {'user_data': {}}
        await buy.start_buy(update, context)
        update.message.reply_text.assert_called_with('به دلیل درخواست‌های زیاد، استفاده شما به مدت 10 دقیقه موقتا مسدود شد.')

if __name__ == '__main__':
    unittest.main()
