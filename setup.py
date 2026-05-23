from setuptools import setup, find_packages

setup(
    name="advanced_ids",  # Package name (lowercase, no spaces)
    version="1.0.0",
    author="Aditya Yadav",
    author_email="aditya.yadav23@pcu.edu.in",
    description="Addressing Data Obsolescence in Network Intrusion Detection A Flow-Based Random Forest Approach",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown", 
    packages=find_packages(where="src"),  
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "joblib",
        "matplotlib",
        "seaborn",
        "shap",
        "xgboost",
        "lightgbm",
        "fastapi",     
        "uvicorn"      
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security :: Intrusion Detection",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "ids-evaluate=src.models.evaluate:main",  # Example CLI entry point for evaluate.py
            # Add more if you want CLI commands for training, API, etc.
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
