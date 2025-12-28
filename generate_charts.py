import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for business-appropriate charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Create charts directory if it doesn't exist
os.makedirs('charts', exist_ok=True)

# Load the dataset
df = pd.read_csv('umico_stores.csv')

print("Generating business intelligence charts...")
print(f"Dataset: {len(df)} stores analyzed\n")

# Chart 1: Store Distribution by Category
print("1. Creating category distribution chart...")
plt.figure(figsize=(12, 7))
category_counts = df['main_category'].value_counts().head(12)
colors = sns.color_palette("husl", len(category_counts))
bars = plt.barh(range(len(category_counts)), category_counts.values, color=colors)
plt.yticks(range(len(category_counts)), category_counts.index)
plt.xlabel('Number of Stores')
plt.title('Store Distribution by Category - Market Concentration Analysis')
plt.gca().invert_yaxis()

# Add value labels
for i, (idx, value) in enumerate(category_counts.items()):
    plt.text(value + 3, i, f'{value} stores ({value/len(df)*100:.1f}%)',
             va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_category_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: Cashback Distribution Overview
print("2. Creating cashback distribution chart...")
plt.figure(figsize=(12, 7))
cashback_dist = df['cashback_percentage'].value_counts().sort_index()
cashback_groups = pd.cut(df['cashback_percentage'],
                         bins=[0, 1, 2, 3, 5, 10, 50],
                         labels=['0-1%', '1-2%', '2-3%', '3-5%', '5-10%', '10%+'],
                         include_lowest=True)
cashback_grouped = cashback_groups.value_counts().sort_index()

colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd', '#8c564b']
bars = plt.bar(range(len(cashback_grouped)), cashback_grouped.values, color=colors)
plt.xticks(range(len(cashback_grouped)), cashback_grouped.index)
plt.ylabel('Number of Stores')
plt.xlabel('Cashback Percentage Range')
plt.title('Cashback Offering Distribution - Incentive Strategy Analysis')

# Add value labels
for i, value in enumerate(cashback_grouped.values):
    plt.text(i, value + 5, f'{value}\n({value/len(df)*100:.1f}%)',
             ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/02_cashback_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Average Cashback by Category
print("3. Creating average cashback by category chart...")
plt.figure(figsize=(12, 7))
cashback_by_cat = df.groupby('main_category')['cashback_percentage'].mean().sort_values(ascending=True).tail(12)
colors = sns.color_palette("RdYlGn", len(cashback_by_cat))
bars = plt.barh(range(len(cashback_by_cat)), cashback_by_cat.values, color=colors)
plt.yticks(range(len(cashback_by_cat)), cashback_by_cat.index)
plt.xlabel('Average Cashback Percentage (%)')
plt.title('Average Cashback by Category - Competitive Incentive Analysis')

# Add value labels
for i, (idx, value) in enumerate(cashback_by_cat.items()):
    plt.text(value + 0.1, i, f'{value:.2f}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/03_cashback_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4: Digital Presence Gap Analysis
print("4. Creating digital presence analysis chart...")
fig, ax = plt.subplots(figsize=(12, 7))

# Calculate percentages for top categories
top_categories = df['main_category'].value_counts().head(10).index
digital_data = []

for cat in top_categories:
    cat_df = df[df['main_category'] == cat]
    total = len(cat_df)
    digital_data.append({
        'Category': cat,
        'Phone': (cat_df['phone_numbers'].notna().sum() / total) * 100,
        'Instagram': (cat_df['instagram'].notna().sum() / total) * 100,
        'Facebook': (cat_df['facebook'].notna().sum() / total) * 100
    })

digital_df = pd.DataFrame(digital_data)
x = np.arange(len(digital_df))
width = 0.25

bars1 = ax.bar(x - width, digital_df['Phone'], width, label='Phone', color='#1f77b4')
bars2 = ax.bar(x, digital_df['Instagram'], width, label='Instagram', color='#ff7f0e')
bars3 = ax.bar(x + width, digital_df['Facebook'], width, label='Facebook', color='#2ca02c')

ax.set_xlabel('Category')
ax.set_ylabel('Percentage of Stores (%)')
ax.set_title('Digital Presence by Category - Communication Channel Gap Analysis')
ax.set_xticks(x)
ax.set_xticklabels([cat[:20] + '...' if len(cat) > 20 else cat for cat in digital_df['Category']],
                    rotation=45, ha='right')
ax.legend()
ax.set_ylim(0, 110)

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        if height > 5:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}%',
                   ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('charts/04_digital_presence_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 5: Rating Engagement Crisis
print("5. Creating rating engagement analysis chart...")
plt.figure(figsize=(12, 7))

# Overall engagement
with_ratings = df['rating'].notna().sum()
without_ratings = df['rating'].isna().sum()

categories = ['Stores with\nCustomer Ratings', 'Stores without\nCustomer Ratings']
values = [with_ratings, without_ratings]
colors = ['#2ca02c', '#d62728']

bars = plt.bar(categories, values, color=colors, width=0.6)
plt.ylabel('Number of Stores')
plt.title('Customer Rating Engagement - Platform Participation Gap')

# Add value labels and percentages
for i, (bar, value) in enumerate(zip(bars, values)):
    plt.text(bar.get_x() + bar.get_width()/2, value + 10,
             f'{value} stores\n({value/len(df)*100:.1f}%)',
             ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.ylim(0, max(values) * 1.15)
plt.tight_layout()
plt.savefig('charts/05_rating_engagement.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 6: Rating Engagement by Category
print("6. Creating rating engagement by category chart...")
plt.figure(figsize=(12, 7))

rating_eng = []
top_cats = df['main_category'].value_counts().head(10).index

for cat in top_cats:
    cat_df = df[df['main_category'] == cat]
    total = len(cat_df)
    with_rating = cat_df['rating'].notna().sum()
    rating_eng.append({
        'Category': cat,
        'Engagement_Rate': (with_rating / total) * 100,
        'Total_Stores': total
    })

rating_eng_df = pd.DataFrame(rating_eng).sort_values('Engagement_Rate', ascending=True)

colors = ['#d62728' if x < 20 else '#ff7f0e' if x < 30 else '#2ca02c'
          for x in rating_eng_df['Engagement_Rate']]
bars = plt.barh(range(len(rating_eng_df)), rating_eng_df['Engagement_Rate'], color=colors)
plt.yticks(range(len(rating_eng_df)),
           [f"{cat[:25]}..." if len(cat) > 25 else cat for cat in rating_eng_df['Category']])
plt.xlabel('Percentage of Stores with Ratings (%)')
plt.title('Rating Engagement by Category - Customer Feedback Participation')

# Add value labels
for i, (idx, row) in enumerate(rating_eng_df.iterrows()):
    plt.text(row['Engagement_Rate'] + 1, i,
             f"{row['Engagement_Rate']:.1f}% ({int(row['Engagement_Rate']*row['Total_Stores']/100)}/{int(row['Total_Stores'])})",
             va='center', fontweight='bold')

plt.xlim(0, max(rating_eng_df['Engagement_Rate']) * 1.3)
plt.tight_layout()
plt.savefig('charts/06_rating_engagement_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 7: Customer Satisfaction (Rating Distribution)
print("7. Creating customer satisfaction chart...")
plt.figure(figsize=(12, 7))

rated_stores = df[df['rating'].notna()]
rating_counts = rated_stores['rating'].value_counts().sort_index()

# Group ratings
rating_groups = pd.cut(rated_stores['rating'],
                       bins=[0, 4.0, 4.5, 4.7, 4.9, 5.0],
                       labels=['Below 4.0', '4.0-4.5', '4.5-4.7', '4.7-4.9', '5.0'],
                       include_lowest=True)
rating_grouped = rating_groups.value_counts().sort_index()

colors = ['#d62728', '#ff7f0e', '#ffdd57', '#a0d911', '#2ca02c']
bars = plt.bar(range(len(rating_grouped)), rating_grouped.values, color=colors)
plt.xticks(range(len(rating_grouped)), rating_grouped.index)
plt.ylabel('Number of Stores')
plt.xlabel('Rating Range')
plt.title(f'Customer Satisfaction Distribution - Average Rating: {rated_stores["rating"].mean():.2f}/5.0')

# Add value labels
for i, value in enumerate(rating_grouped.values):
    pct = (value / len(rated_stores)) * 100
    plt.text(i, value + 0.5, f'{value}\n({pct:.1f}%)',
             ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/07_customer_satisfaction.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 8: Store Expansion Analysis (Multi-location vs Single-location)
print("8. Creating store expansion analysis chart...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Multi vs Single location
multi_location = df[df['total_locations'] > 1]
single_location = df[df['total_locations'] == 1]

categories = ['Multi-Location\nChains', 'Single-Location\nStores']
values = [len(multi_location), len(single_location)]
colors = ['#1f77b4', '#ff7f0e']

bars = ax1.bar(categories, values, color=colors, width=0.6)
ax1.set_ylabel('Number of Stores')
ax1.set_title('Store Expansion Model Distribution')

for bar, value in zip(bars, values):
    ax1.text(bar.get_x() + bar.get_width()/2, value + 10,
             f'{value} stores\n({value/len(df)*100:.1f}%)',
             ha='center', va='bottom', fontweight='bold')

ax1.set_ylim(0, max(values) * 1.15)

# Right: Top 10 multi-location stores
top_locations = df.nlargest(10, 'total_locations')[['store_name', 'total_locations']].sort_values('total_locations')
bars = ax2.barh(range(len(top_locations)), top_locations['total_locations'],
                color=sns.color_palette("viridis", len(top_locations)))
ax2.set_yticks(range(len(top_locations)))
ax2.set_yticklabels([name[:20] + '...' if len(name) > 20 else name
                      for name in top_locations['store_name']])
ax2.set_xlabel('Number of Locations')
ax2.set_title('Top 10 Stores by Location Count')

for i, (idx, row) in enumerate(top_locations.iterrows()):
    ax2.text(row['total_locations'] + 2, i, f"{int(row['total_locations'])}",
             va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_store_expansion_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 9: High-Value Incentive Opportunities
print("9. Creating high-value incentive analysis chart...")
plt.figure(figsize=(12, 7))

# Group by cashback ranges and count stores
cashback_ranges = [
    ('0-1%', 0, 1),
    ('1-2%', 1, 2),
    ('2-3%', 2, 3),
    ('3-5%', 3, 5),
    ('5-10%', 5, 10),
    ('10%+', 10, 50)
]

cashback_data = []
for label, min_val, max_val in cashback_ranges:
    count = len(df[(df['cashback_percentage'] > min_val) & (df['cashback_percentage'] <= max_val)])
    cashback_data.append({'Range': label, 'Count': count})

cashback_summary = pd.DataFrame(cashback_data)

colors = ['#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#2ca02c']
bars = plt.bar(range(len(cashback_summary)), cashback_summary['Count'], color=colors)
plt.xticks(range(len(cashback_summary)), cashback_summary['Range'])
plt.ylabel('Number of Stores')
plt.xlabel('Cashback Percentage Range')
plt.title('Cashback Strategy Distribution - Competitive Positioning')

# Add value labels with percentages
for i, row in cashback_summary.iterrows():
    plt.text(i, row['Count'] + 5,
             f"{row['Count']}\n({row['Count']/len(df)*100:.1f}%)",
             ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/09_cashback_strategy.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 10: Category Market Share and Opportunity
print("10. Creating market share analysis chart...")
plt.figure(figsize=(14, 8))

category_summary = df['main_category'].value_counts().head(12)
colors = sns.color_palette("Set3", len(category_summary))

bars = plt.bar(range(len(category_summary)), category_summary.values, color=colors)
plt.xticks(range(len(category_summary)),
           [cat[:15] + '...' if len(cat) > 15 else cat for cat in category_summary.index],
           rotation=45, ha='right')
plt.ylabel('Number of Stores')
plt.xlabel('Category')
plt.title('Market Share by Category - Strategic Opportunity Analysis')

# Add value labels with percentages
for i, (cat, value) in enumerate(category_summary.items()):
    plt.text(i, value + 2,
             f'{value}\n({value/len(df)*100:.1f}%)',
             ha='center', fontweight='bold', fontsize=9)

plt.ylim(0, max(category_summary.values) * 1.15)
plt.tight_layout()
plt.savefig('charts/10_market_share.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 11: Digital Strategy by Store Scale
print("11. Creating digital strategy by scale chart...")
fig, ax = plt.subplots(figsize=(12, 7))

# Segment stores by scale
df['store_scale'] = pd.cut(df['total_locations'],
                           bins=[0, 1, 5, 20, 200],
                           labels=['Single (1)', 'Small Chain (2-5)', 'Medium Chain (6-20)', 'Large Chain (20+)'])

scale_digital = []
for scale in ['Single (1)', 'Small Chain (2-5)', 'Medium Chain (6-20)', 'Large Chain (20+)']:
    scale_df = df[df['store_scale'] == scale]
    if len(scale_df) > 0:
        total = len(scale_df)
        scale_digital.append({
            'Scale': scale,
            'Phone': (scale_df['phone_numbers'].notna().sum() / total) * 100,
            'Instagram': (scale_df['instagram'].notna().sum() / total) * 100,
            'Facebook': (scale_df['facebook'].notna().sum() / total) * 100,
            'Count': total
        })

scale_df = pd.DataFrame(scale_digital)
x = np.arange(len(scale_df))
width = 0.25

bars1 = ax.bar(x - width, scale_df['Phone'], width, label='Phone', color='#1f77b4')
bars2 = ax.bar(x, scale_df['Instagram'], width, label='Instagram', color='#ff7f0e')
bars3 = ax.bar(x + width, scale_df['Facebook'], width, label='Facebook', color='#2ca02c')

ax.set_xlabel('Store Scale')
ax.set_ylabel('Percentage (%)')
ax.set_title('Digital Presence by Store Scale - Channel Strategy Analysis')
ax.set_xticks(x)
ax.set_xticklabels([f"{row['Scale']}\n({int(row['Count'])} stores)"
                     for _, row in scale_df.iterrows()])
ax.legend()
ax.set_ylim(0, 110)

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        if height > 5:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}%',
                   ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('charts/11_digital_strategy_by_scale.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 12: Rating Performance vs Store Characteristics
print("12. Creating rating performance analysis chart...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Average rating by category (for categories with enough ratings)
rating_by_cat = df[df['rating'].notna()].groupby('main_category').agg({
    'rating': ['mean', 'count']
}).round(2)
rating_by_cat.columns = ['avg_rating', 'count']
rating_by_cat = rating_by_cat[rating_by_cat['count'] >= 3].sort_values('avg_rating', ascending=True).tail(10)

colors = ['#d62728' if x < 4.5 else '#ff7f0e' if x < 4.75 else '#2ca02c'
          for x in rating_by_cat['avg_rating']]
bars = ax1.barh(range(len(rating_by_cat)), rating_by_cat['avg_rating'], color=colors)
ax1.set_yticks(range(len(rating_by_cat)))
ax1.set_yticklabels([idx[:20] + '...' if len(idx) > 20 else idx for idx in rating_by_cat.index])
ax1.set_xlabel('Average Rating')
ax1.set_title('Average Customer Rating by Category')
ax1.set_xlim(4.0, 5.1)

for i, (idx, row) in enumerate(rating_by_cat.iterrows()):
    ax1.text(row['avg_rating'] + 0.02, i,
             f"{row['avg_rating']:.2f} ({int(row['count'])} reviews)",
             va='center', fontweight='bold', fontsize=9)

# Right: Stores needing rating engagement push
engagement_priority = []
for cat in df['main_category'].value_counts().head(10).index:
    cat_df = df[df['main_category'] == cat]
    total = len(cat_df)
    rated = cat_df['rating'].notna().sum()
    unrated = total - rated
    engagement_priority.append({
        'Category': cat,
        'Unrated': unrated,
        'Total': total
    })

engagement_df = pd.DataFrame(engagement_priority).sort_values('Unrated', ascending=True)
bars = ax2.barh(range(len(engagement_df)), engagement_df['Unrated'], color='#d62728')
ax2.set_yticks(range(len(engagement_df)))
ax2.set_yticklabels([cat[:20] + '...' if len(cat) > 20 else cat
                      for cat in engagement_df['Category']])
ax2.set_xlabel('Number of Stores Without Ratings')
ax2.set_title('Rating Engagement Gap by Category')

for i, (idx, row) in enumerate(engagement_df.iterrows()):
    ax2.text(row['Unrated'] + 2, i,
             f"{int(row['Unrated'])} ({row['Unrated']/row['Total']*100:.0f}%)",
             va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('charts/12_rating_performance.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("CHART GENERATION COMPLETE")
print("="*60)
print(f"\nGenerated 12 business intelligence charts in 'charts/' directory:")
print("  1. Category Distribution")
print("  2. Cashback Distribution")
print("  3. Cashback by Category")
print("  4. Digital Presence by Category")
print("  5. Rating Engagement")
print("  6. Rating Engagement by Category")
print("  7. Customer Satisfaction")
print("  8. Store Expansion Analysis")
print("  9. Cashback Strategy")
print(" 10. Market Share")
print(" 11. Digital Strategy by Scale")
print(" 12. Rating Performance")
print("\nAll charts saved as high-resolution PNG files (300 DPI)")
print("="*60)
