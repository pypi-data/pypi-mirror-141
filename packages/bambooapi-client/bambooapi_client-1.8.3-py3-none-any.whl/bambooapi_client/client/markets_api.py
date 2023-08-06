# noqa: D100
from datetime import datetime

from bambooapi_client.api.markets_api import MarketsApi as _MarketsApi
from bambooapi_client.model.market_prices_units import MarketPricesUnits
from bambooapi_client.model.ramping import Ramping

import pandas as pd


class MarketsApi(object):
    """Implementation for '/v1/sites' endpoints."""

    def __init__(self, bambooapi_client):
        self._bambooapi_client = bambooapi_client
        self._api_instance = _MarketsApi(bambooapi_client.api_client)

    def get_market_prices(  # noqa: D102
        self,
        market_id: int,
        start_date: datetime,
        end_date: datetime,
        units: MarketPricesUnits = MarketPricesUnits('MW').to_str(),
    ) -> pd.DataFrame:
        response = self._api_instance.get_market_prices(
            market_id=market_id,
            start_date=start_date,
            end_date=end_date,
            units=units,
        )
        if response:
            return pd.DataFrame.from_records(
                response.get('series', []),
                index='time',
            )
        else:
            return pd.DataFrame()

    def insert_energy_market_prices(
        self,
        market_id: int,
        market_prices: pd.DataFrame,
    ) -> None:
        """Insert market prices from a dataframe.

        Dataframe must be indexed by timezone-aware UTC-datetime,
        with index name `time` and with a column named `energy_price`

        Example
        -------
        time,energy_price
        2021-05-01 00:00:00+00:00,100.0
        2021-05-01 00:15:00+00:00,92.6
        2021-05-01 00:30:00+00:00,43.4

        Raises
        ------
        ValueError:
            If Dataframe has no columns or columns are not the expected ones.
        """
        self._validate_energy_market_prices(dataframe=market_prices)

        data_points = market_prices.reset_index().to_dict(orient='records')
        return self._api_instance.insert_market_prices(
            market_id=market_id,
            market_price=data_points,
        )

    def insert_flexibility_market_prices(
        self,
        market_id: int,
        market_prices: pd.DataFrame,
    ) -> None:
        """Insert market prices from a dataframe.

        Dataframe must have the following structure:
        * Indexed by timezone-aware UTC-datetime, with index name `time`
        * At least one of the columns `energy_price_up`, `energy_price_down` or
          `capacity_price` must exist.

        Example
        -------
        time,energy_price_up,energy_price_down,capacity_price
        2021-05-01 00:00:00+00:00,100.0,70.0,23.0
        2021-05-01 00:15:00+00:00,92.6,42.6,35.3
        2021-05-01 00:30:00+00:00,43.4,13.4,26.5

        Raises
        ------
        ValueError:
            If Dataframe has no columns or columns are not the expected ones.
        """
        self._validate_flexibility_market_prices(dataframe=market_prices)

        for column in market_prices.columns:
            df = market_prices[[column]]
            kwargs = {}
            if column == 'energy_price_up':
                kwargs.update({'ramping': Ramping('ramp_up').to_str()})
                df = df.rename(columns={'energy_price_up': 'energy_price'})
            elif column == 'energy_price_down':
                kwargs.update({'ramping': Ramping('ramp_down').to_str()})
                df = df.rename(columns={'energy_price_down': 'energy_price'})

            data_points = df.reset_index().to_dict(orient='records')
            self._api_instance.insert_market_prices(
                market_id=market_id,
                market_price=data_points,
                **kwargs,
            )

    @classmethod
    def _validate_energy_market_prices(cls, dataframe: pd.DataFrame) -> None:
        expected_columns = ['energy_price']
        if dataframe.columns != expected_columns:
            raise ValueError(
                f'Invalid columns. Expected columns {expected_columns}'
            )

    @classmethod
    def _validate_flexibility_market_prices(
        cls,
        dataframe: pd.DataFrame,
    ) -> None:
        expected_columns = {
            'energy_price_up',
            'energy_price_down',
            'capacity_price',
        }
        if (
            len(dataframe.columns) == 0
            or not set(dataframe.columns).issubset(expected_columns)
        ):
            raise ValueError(
                f'Invalid columns. At least one of {expected_columns}'
            )
