from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting StartupTracker...")
    print("📊 Customer Analytics for Early-Stage Startups")
    print("🌐 Open your browser to: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
