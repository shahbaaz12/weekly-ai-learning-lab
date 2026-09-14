# What this file does: turns the product catalog JSON into documents at three levels of detail.
"""Catalog -> product documents, variant documents, and subcategory summaries."""

import json
from collections import defaultdict
from pathlib import Path

from langchain_core.documents import Document


# The catalog lives in the shared Week 10 docs folder, one level up.
CATALOG_PATH = (
    Path(__file__).parent.parent / "docs" / "products2" / "Hierarchical_Product_Catalog.json"
)


def load_products() -> list[dict]:
    """Read the catalog and return its product list."""
    with open(CATALOG_PATH, encoding="utf-8") as file:
        return json.load(file)["products"]


# The JSON holds dicts and lists. Flattening them into lines keeps the embedded
# text close to natural language and makes a retrieved document readable as-is.
def dict_to_text(data: dict) -> str:
    return "\n".join(f"- {key}: {value}" for key, value in data.items())


def list_to_text(items: list) -> str:
    return "\n".join(f"- {item}" for item in items)


def variants_to_text(variants: list) -> str:
    if not variants:
        return "No variants"

    return "\n".join(
        f"- {v['variant_name']} ({v['variant_id']}): {v['description']}" for v in variants
    )


def error_codes_to_text(error_codes: list) -> str:
    return "\n".join(
        f"- {e['code']}: {e['meaning']} | Resolution: {e['resolution']}"
        for e in error_codes
    )


def product_documents(products: list[dict]) -> list[Document]:
    """One document per product, holding everything the catalog says about it."""
    documents = []

    for product in products:
        text = f"""
Product Name: {product["product_name"]}
Product ID: {product["product_id"]}
Category: {product["category"]}
Subcategory: {product["subcategory"]}
Manufacturer: {product["manufacturer"]}
Starting Price: {product["starting_price_usd"]}

Description:
{product["description"]}

Specifications:
{dict_to_text(product["specifications"])}

Quick Start:
{list_to_text(product["quick_start"])}

How To Use:
{list_to_text(product["how_to_use"])}

Error Codes:
{error_codes_to_text(product["error_codes"])}

Variants:
{variants_to_text(product["variants"])}
""".strip()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "level": "product",
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "category": product["category"],
                    "subcategory": product["subcategory"],
                    "manufacturer": product["manufacturer"],
                },
            )
        )

    return documents


def variant_documents(products: list[dict]) -> list[Document]:
    """One document per variant. parent_product_id keeps the link to its product."""
    documents = []

    for product in products:
        for variant in product["variants"]:
            text = f"""
Variant Name: {variant["variant_name"]}
Variant ID: {variant["variant_id"]}

Parent Product: {product["product_name"]}
Parent Product ID: {product["product_id"]}

Category: {product["category"]}
Subcategory: {product["subcategory"]}

Price: {variant["price_usd"]}

Description:
{variant["description"]}
""".strip()

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "level": "variant",
                        "variant_id": variant["variant_id"],
                        "variant_name": variant["variant_name"],
                        "parent_product_id": product["product_id"],
                        "parent_product_name": product["product_name"],
                        "category": product["category"],
                        "subcategory": product["subcategory"],
                    },
                )
            )

    return documents


def subcategory_documents(products: list[dict]) -> list[Document]:
    """One summary per subcategory, so a broad question can see every product at once."""
    groups = defaultdict(list)

    for product in products:
        groups[(product["category"], product["subcategory"])].append(product)

    documents = []

    for (category, subcategory), group in groups.items():
        summaries = [
            f"""
Product: {product["product_name"]}
Product ID: {product["product_id"]}
Manufacturer: {product["manufacturer"]}
Starting Price: {product["starting_price_usd"]}
Description: {product["description"]}
Variant Count: {len(product["variants"])}
""".strip()
            for product in group
        ]
        manufacturers = ", ".join(sorted({product["manufacturer"] for product in group}))
        product_block = "\n\n".join(summaries)

        text = f"""
Category:
{category}

Subcategory:
{subcategory}

Total Products:
{len(group)}

Manufacturers:
{manufacturers}

Products:

{product_block}
""".strip()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "level": "subcategory",
                    "category": category,
                    "subcategory": subcategory,
                    "product_count": len(group),
                },
            )
        )

    return documents
