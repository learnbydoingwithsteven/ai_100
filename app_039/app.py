"""
AI Application 39 AI Application
AI-powered solution for use case 39
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import time
import os

plt.style.use('seaborn-v0_8-darkgrid')

class AiApplication39AI:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def generate_data(self, n_samples=1000):
        """Generate synthetic data"""
        print(f"\n📊 Generating {n_samples} samples...")
        np.random.seed(42)
        
        n_features = 15
        X = np.random.randn(n_samples, n_features)
        y = X.sum(axis=1) + np.random.randn(n_samples) * 0.5
        
        print(f"✅ Generated {n_samples} samples")
        return X, y
    
    def train_model(self, X_train, y_train):
        """Train model"""
        print("\n🎓 Training...")
        start_time = time.time()
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        return time.time() - start_time
    
    def evaluate(self, X_test, y_test):
        """Evaluate"""
        X_test_scaled = self.scaler.transform(X_test)
        y_pred = self.model.predict(X_test_scaled)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"\n📈 R² Score: {r2:.4f}")
        print(f"📈 MAE: {mae:.4f}")
        print(f"📈 RMSE: {rmse:.4f}")
        
        return y_pred, r2, mae, rmse
    
    def visualize(self, y_test, y_pred, r2, mae):
        """Visualize"""
        fig = plt.figure(figsize=(16, 6))
        
        ax1 = plt.subplot(1, 3, 1)
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title(f'Predictions (R²={r2:.3f})', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        ax2 = plt.subplot(1, 3, 2)
        residuals = y_test - y_pred
        plt.hist(residuals, bins=30, alpha=0.7, edgecolor='black')
        plt.xlabel('Residual')
        plt.ylabel('Frequency')
        plt.title('Residual Distribution', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        ax3 = plt.subplot(1, 3, 3)
        importance = self.model.feature_importances_
        plt.bar(range(len(importance)), importance, alpha=0.7)
        plt.xlabel('Feature')
        plt.ylabel('Importance')
        plt.title('Feature Importance', fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        os.makedirs('outputs', exist_ok=True)
        plt.savefig('outputs/results.png', dpi=300, bbox_inches='tight')
        print("✅ Saved to: outputs/results.png")
        plt.show()
    
    def run(self):
        """Run analysis"""
        print("\n" + "="*70)
        print("🤖 AI Application 39 AI")
        print("="*70)
        
        X, y = self.generate_data(1000)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.train_model(X_train, y_train)
        y_pred, r2, mae, rmse = self.evaluate(X_test, y_test)
        self.visualize(y_test, y_pred, r2, mae)
        
        print("\n✅ COMPLETE!")

if __name__ == "__main__":
    ai = AiApplication39AI()
    ai.run()
