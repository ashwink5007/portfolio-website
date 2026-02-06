import { ExternalLink, Github, Shield, Heart } from "lucide-react";

const projects = [
  {
    title: "VoiceShield",
    subtitle: "Real-Time DeepFake Voice Detection System",
    icon: Shield,
    techStack: ["Python", "Librosa", "PyTorch", "Scikit-Learn", "Transformers", "SpeechBrain", "Streamlit"],
    description: "Built an AI-driven system to detect AI-generated (deepfake) voice commands to secure voice-enabled systems and smart vehicles. Combined MFCC, pitch, jitter features with deep embeddings from Wav2Vec2 to achieve robust detection. Implemented real-time prediction pipeline and lightweight deployment optimizations.",
    color: "from-accent to-primary",
  },
  {
    title: "CharityConnect",
    subtitle: "Charity Community Platform System",
    icon: Heart,
    techStack: ["React.js", "Node.js", "Express.js", "MongoDB", "JWT", "REST APIs"],
    description: "Built a MERN-based platform connecting donors with verified NGOs to ensure transparent and secure charitable contributions. Developed frontend interfaces and backend APIs with JWT-based authentication, role-based access, and NGO verification workflows. Implemented scalable features such as recommendations and real-time messaging.",
    color: "from-primary to-accent",
  },
];

const Projects = () => {
  return (
    <section id="projects" className="py-20 md:py-28 bg-background">
      <div className="container mx-auto px-6">
        <div className="max-w-5xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Featured <span className="text-accent">Projects</span>
            </h2>
            <div className="w-20 h-1 bg-accent mx-auto rounded-full" />
          </div>

          {/* Projects */}
          <div className="space-y-8">
            {projects.map((project, index) => (
              <div
                key={project.title}
                className="group bg-card rounded-2xl overflow-hidden shadow-card hover:shadow-xl transition-all duration-500 border border-border hover:border-accent/30"
              >
                <div className="flex flex-col lg:flex-row">
                  {/* Icon Section */}
                  <div className={`lg:w-1/3 p-8 flex items-center justify-center bg-gradient-to-br ${project.color}`}>
                    <div className="w-24 h-24 md:w-32 md:h-32 rounded-2xl bg-white/10 backdrop-blur flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
                      <project.icon size={48} className="text-white" />
                    </div>
                  </div>

                  {/* Content Section */}
                  <div className="lg:w-2/3 p-6 md:p-8">
                    <div className="mb-4">
                      <h3 className="text-xl md:text-2xl font-bold text-foreground mb-1">
                        {project.title}
                      </h3>
                      <p className="text-accent font-medium text-sm">
                        {project.subtitle}
                      </p>
                    </div>

                    <p className="text-muted-foreground text-sm md:text-base leading-relaxed mb-6">
                      {project.description}
                    </p>

                    {/* Tech Stack */}
                    <div className="flex flex-wrap gap-2 mb-6">
                      {project.techStack.map((tech) => (
                        <span
                          key={tech}
                          className="px-3 py-1 text-xs font-medium bg-secondary text-secondary-foreground rounded-full"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>

                    {/* Links */}
                    <div className="flex gap-3">
                      <a
                        href="https://github.com/ashwink5007/voiceshielddetection"
                        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium bg-accent text-accent-foreground rounded-lg hover:bg-accent-hover transition-colors"
                      >
                        <Github size={16} />
                        View Code
                      </a>
                      <a
                        href="#"
                        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium border border-border text-foreground rounded-lg hover:bg-secondary transition-colors"
                      >
                        <ExternalLink size={16} />
                        Live Demo
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Projects;
