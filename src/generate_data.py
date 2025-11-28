# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Générateur de données synthétiques (inscriptions + commandes) pour l'étude de rétention.

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

DEFAULT_START = pd.Timestamp("2023-01-01")
DEFAULT_END = pd.Timestamp("2024-12-31")


@dataclass
class GenerationConfig:
    """Bundle the tunable knobs to keep the CLI and tests in sync."""

    n_users: int = 600
    seed: int = 42
    start: pd.Timestamp = DEFAULT_START
    end: pd.Timestamp = DEFAULT_END


def generate_users(config: GenerationConfig) -> pd.DataFrame:
    """Crée un DataFrame d’utilisateurs avec dates d’inscription réparties sur la période."""
    rng = np.random.default_rng(config.seed)
    signup_dates = pd.to_datetime(
        rng.integers(
            config.start.value // 10**9,
            config.end.value // 10**9,
            size=config.n_users,
        ),
        unit="s",
    )
    users = (
        pd.DataFrame({"user_id": range(1, config.n_users + 1), "signup_date": signup_dates})
        .sort_values("signup_date")
        .reset_index(drop=True)
    )
    return users


def generate_orders(users: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Crée un jeu de commandes synthétiques à partir des utilisateurs fournis."""
    rng = np.random.default_rng(seed + 1)
    orders = []
    order_id = 1
    for _, row in users.iterrows():
        first = row.signup_date + pd.Timedelta(days=int(rng.integers(0, 20)))
        k = int(rng.integers(1, 6))
        current_date = first
        for _ in range(k):
            amount = float(np.clip(rng.normal(50, 20), 5, 300))
            orders.append(
                [
                    order_id,
                    int(row.user_id),
                    current_date.normalize(),
                    round(amount, 2),
                ]
            )
            order_id += 1
            if rng.random() < 0.5:
                break
            current_date = current_date + pd.Timedelta(days=int(rng.integers(15, 60)))

    orders_df = (
        pd.DataFrame(orders, columns=["order_id", "user_id", "order_date", "amount"])
        .sort_values("order_date")
        .reset_index(drop=True)
    )
    return orders_df


def generate_dataset(config: GenerationConfig | None = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Assemble les jeux `users` et `orders` en appliquant la configuration fournie."""
    cfg = config or GenerationConfig()
    users = generate_users(cfg)
    orders = generate_orders(users, cfg.seed)
    return users, orders


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic cohort data.")
    parser.add_argument(
        "--n-users",
        type=int,
        default=600,
        help="Number of synthetic users to simulate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--users-output",
        default="data/users.csv",
        help="Output path for the users CSV.",
    )
    parser.add_argument(
        "--orders-output",
        default="data/orders.csv",
        help="Output path for the orders CSV.",
    )
    args = parser.parse_args()

    cfg = GenerationConfig(n_users=args.n_users, seed=args.seed)
    users, orders = generate_dataset(cfg)

    users_path = Path(args.users_output)
    orders_path = Path(args.orders_output)
    users_path.parent.mkdir(exist_ok=True, parents=True)
    orders_path.parent.mkdir(exist_ok=True, parents=True)

    users.to_csv(users_path, index=False)
    orders.to_csv(orders_path, index=False)

    print(f"Saved {len(users)} users to {users_path}")
    print(f"Saved {len(orders)} orders to {orders_path}")


if __name__ == "__main__":
    main()
