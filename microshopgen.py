#!/usr/bin/env python3
"""
MicroShopGen: An e-commerce Software Product Line Generator

A CLI tool to select and configure features for an e-commerce system based on a microservices architecture.
Made as a requirement for the Software Product Line (SPL) course at the Federal University of Alagoas (UFAL).
Students:   Victor Alexandre da Rocha Monteiro Miranda
            Victor Hugo Sampaio Lima
"""

import os
import json
import argparse
from typing import Dict, List

FEATURES = {
    "core": {
        "description": "Core services required for basic e-commerce functionality",
        "components": {
            "gateway": {
                "name": "API Gateway",
                "description": "Entry point for all client requests",
                "required": True,
            },
            "user": {
                "name": "User Service",
                "description": "User authentication and profile management",
                "required": True,
            },
            "catalog": {
                "name": "Catalog Service",
                "description": "Product catalog management",
                "required": True,
            },
            "cart": {
                "name": "Cart Service",
                "description": "Shopping cart management",
                "required": True,
            },
            "orders": {
                "name": "Order Service",
                "description": "Order processing and management",
                "required": True,
            },
            "payments": {
                "name": "Payment Service",
                "description": "Payment processing",
                "required": True,
            },
            "inventory": {
                "name": "Inventory Service",
                "description": "Stock management",
                "required": True,
            },
        },
    },
    "optional": {
        "description": "Optional services to enhance e-commerce functionality",
        "components": {
            "reviews": {
                "name": "Reviews Service",
                "description": "Product reviews and ratings",
                "required": False,
            },
            "discounts": {
                "name": "Discounts Service",
                "description": "Promotional offers and discount management",
                "required": False,
            },
            "admin": {
                "name": "Admin Dashboard Service",
                "description": "Administrative interface backend",
                "required": False,
            },
        },
    },
}


class FeatureSelector:
    """Handles feature selection and configuration for the SPL"""

    def __init__(self, config_file="ecommerce_config.json"):
        self.config_file = config_file
        self.selected_features = self._load_config()

    def _load_config(self) -> Dict[str, List[str]]:
        """Load existing configuration or create default"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            default_config = {"core": [], "optional": []}
            for category, data in FEATURES.items():
                for component_id, component in data["components"].items():
                    if component.get("required", False):
                        default_config[category].append(component_id)
            return default_config

    def save_config(self):
        """Save the current configuration to file"""
        with open(self.config_file, "w") as f:
            json.dump(self.selected_features, f, indent=2)
        print(f"Configuration saved to {self.config_file}")

    def display_features(self):
        """Display all available features with selection status"""
        print("\n=== E-COMMERCE MICROSERVICE FEATURES ===\n")

        for category, data in FEATURES.items():
            print(f"\n{category.upper()}: {data['description']}")
            print("-" * 50)

            for component_id, component in data["components"].items():
                selected = (
                    "✓" if component_id in self.selected_features[category] else " "
                )
                required = "[Required]" if component.get("required", False) else ""
                print(f"[{selected}] {component_id}: {component['name']} {required}")
                print(f"    {component['description']}")

        print("\n")

    def toggle_feature(self, category: str, feature_id: str) -> bool:
        """Toggle a feature on or off"""
        if (
            category not in FEATURES
            or feature_id not in FEATURES[category]["components"]
        ):
            print(f"Error: Feature '{feature_id}' in category '{category}' not found.")
            return False

        if FEATURES[category]["components"][feature_id].get("required", False):
            print(f"Error: Cannot disable required feature '{feature_id}'.")
            return False

        if feature_id in self.selected_features[category]:
            self.selected_features[category].remove(feature_id)
            print(f"Disabled: {feature_id}")
        else:
            self.selected_features[category].append(feature_id)
            print(f"Enabled: {feature_id}")

        return True

    def interactive_cli(self):
        """Run an interactive CLI for feature selection"""
        while True:
            self.display_features()
            print("Commands:")
            print("  toggle <category> <feature_id> - Toggle a feature on/off")
            print("  save - Save current configuration")
            print("  exit - Exit without saving")
            print("  done - Save and exit")

            cmd = input("\nEnter command: ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "exit":
                return False
            elif cmd[0] == "save":
                self.save_config()
            elif cmd[0] == "done":
                self.save_config()
                return True
            elif cmd[0] == "toggle" and len(cmd) == 3:
                self.toggle_feature(cmd[1], cmd[2])
            else:
                print("Invalid command. Try again.")


def generate_microservices(config_file: str, output_dir: str):
    from generators.inventory import InventoryServiceGenerator

    # todo: repeat with all other generators
    generators = {
        "inventory": InventoryServiceGenerator,
    }

    selector = FeatureSelector(config_file)
    for feature in (
        selector.selected_features["core"] + selector.selected_features["optional"]
    ):
        if feature in generators:
            generator = generators[feature]()
            generator.generate(output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="E-commerce Software Product Line Generator"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="ecommerce_config.json",
        help="Configuration file path",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate selected microservices",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated",
        help="Output directory for the generated microservices",
    )

    args = parser.parse_args()

    if args.generate:
        generate_microservices(args.config, args.output_dir)
        return

    selector = FeatureSelector(config_file=args.config)

    if selector.interactive_cli():
        print("\nFeature selection complete!")
        print(f"Configuration saved to {args.config}")
        print(
            "\nYou can now use this configuration to generate the microservice project."
        )


if __name__ == "__main__":
    main()
