import Generator from '../components/Generator';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center relative p-4">
      <div className="glow-bg" />

      <div className="z-10 w-full max-w-4xl flex flex-col items-center space-y-8 mb-8">
        <div className="text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter">
            Craft Your <span className="gradient-text">Digital Persona</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto">
            AI-powered bio generation for the modern creator.
            Trained on high-impact social profiles to deliver the perfect first impression.
          </p>
        </div>
      </div>

      <div className="z-10 w-full">
        <Generator />
      </div>

      <footer className="absolute bottom-4 text-center text-gray-600 text-sm z-10">
        Powered by GPT-2 & Next.js
      </footer>
    </main>
  );
}
