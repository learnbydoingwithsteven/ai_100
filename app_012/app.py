"""
AI Application 12 AI Application
AI-powered solution for use case 12
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import time
import os

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class AiApplication12AI:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.classes = ['Normal', 'Abnormal', 'Critical']
        
    def generate_data(self, n_samples=1000):
        """Generate synthetic data"""
        print(f"\n📊 Generating {n_samples} samples...")
        np.random.seed(42)
        
        n_features = 20
        X = np.random.randn(n_samples, n_features)
        y = np.random.randint(0, len(self.classes), n_samples)
        
        print(f"✅ Generated {n_samples} samples with {n_features} features")
        return X, y
    
    def train_model(self, X_train, y_train):
        """Train the model"""
        print("\n🎓 Training model...")
        start_time = time.time()
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        training_time = time.time() - start_time
        print(f"✅ Training completed in {training_time:.2f}s")
        
        return training_time
    
    def evaluate(self, X_test, y_test):
        """Evaluate model"""
        print("\n📈 Evaluating model...")
        
        X_test_scaled = self.scaler.transform(X_test)
        y_pred = self.model.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        print("\n" + "="*70)
        print(classification_report(y_test, y_pred, target_names=self.classes))
        print(f"\nOverall Accuracy: {accuracy:.2%}")
        
        return y_pred, cm, accuracy
    
    def visualize(self, X_test, y_test, y_pred, cm, training_time):
        """Create visualizations"""
        print("\n🎨 Creating visualizations...")
        
        fig = plt.figure(figsize=(16, 10))
        
        # Confusion Matrix
        ax1 = plt.subplot(2, 3, 1)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.classes, yticklabels=self.classes)
        plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # Accuracy by Class
        ax2 = plt.subplot(2, 3, 2)
        class_acc = cm.diagonal() / cm.sum(axis=1)
        plt.bar(range(len(self.classes)), class_acc, alpha=0.7)
        plt.xticks(range(len(self.classes)), self.classes, rotation=45, ha='right')
        plt.ylabel('Accuracy')
        plt.title('Per-Class Accuracy', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Feature Importance
        ax3 = plt.subplot(2, 3, 3)
        importance = self.model.feature_importances_
        plt.bar(range(len(importance)), importance, alpha=0.7)
        plt.xlabel('Feature Index')
        plt.ylabel('Importance')
        plt.title('Feature Importance', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Class Distribution
        ax4 = plt.subplot(2, 3, 4)
        unique, counts = np.unique(y_test, return_counts=True)
        plt.pie(counts, labels=[self.classes[i] for i in unique], autopct='%1.1f%%')
        plt.title('Test Set Distribution', fontsize=14, fontweight='bold')
        
        # Prediction Confidence
        ax5 = plt.subplot(2, 3, 5)
        X_test_scaled = self.scaler.transform(X_test)
        proba = self.model.predict_proba(X_test_scaled)
        max_proba = np.max(proba, axis=1)
        plt.hist(max_proba, bins=30, alpha=0.7, edgecolor='black')
        plt.xlabel('Confidence')
        plt.ylabel('Frequency')
        plt.title('Prediction Confidence', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Summary Stats
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        stats_text = f"""
        📊 PERFORMANCE SUMMARY
        
        Total Samples: {len(y_test)}
        Classes: {len(self.classes)}
        
        Overall Accuracy: {accuracy_score(y_test, y_pred):.2%}
        Training Time: {training_time:.2f}s
        
        Best Class: {self.classes[class_acc.argmax()]}
        Best Accuracy: {class_acc.max():.2%}
        """
        ax6.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
                verticalalignment='center')
        
        plt.tight_layout()
        
        os.makedirs('outputs', exist_ok=True)
        output_path = 'outputs/results.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to: {output_path}")
        plt.show()
    
    def run(self):
        """Run complete analysis"""
        print("\n" + "="*70)
        print("🤖 AI Application 12 AI - COMPREHENSIVE ANALYSIS")
        print("="*70)
        
        X, y = self.generate_data(n_samples=1000)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        training_time = self.train_model(X_train, y_train)
        y_pred, cm, accuracy = self.evaluate(X_test, y_test)
        self.visualize(X_test, y_test, y_pred, cm, training_time)
        
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE!")
        print("="*70)

if __name__ == "__main__":
    ai = AiApplication12AI()
    ai.run()
