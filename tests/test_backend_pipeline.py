import sys, os

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from backend.pipeline import ETFPipeline

pipeline = ETFPipeline("QQQ")
result = pipeline.run()

print("\n=== Backend Pipeline Output ===")
for key, value in result.items():
    print(f"{key}: {value}\n")
