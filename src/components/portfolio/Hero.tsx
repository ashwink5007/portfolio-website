import { ArrowDown, Github, Linkedin, Mail, MapPin, Phone } from "lucide-react";

const Hero = () => {
  const handleScrollToAbout = () => {
    const element = document.querySelector("#about");
    element?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="min-h-screen flex items-center justify-center bg-hero-gradient text-primary-foreground relative overflow-hidden">
      {/* Subtle animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-accent/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/3 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl animate-float" style={{ animationDelay: "1.5s" }} />
      </div>

      <div className="container mx-auto px-6 py-20 relative z-10">
        <div className="max-w-3xl mx-auto text-center">
          {/* Greeting */}
          <p className="animate-fade-up text-accent font-medium mb-4 text-sm md:text-base tracking-wide">
            Hello, I'm
          </p>

          {/* Name */}
          <h1 className="animate-fade-up-delay-1 text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 tracking-tight">
            Alagar Ashwin K
          </h1>

          {/* Role */}
          <p className="animate-fade-up-delay-2 text-lg sm:text-xl md:text-2xl text-primary-foreground/80 mb-8 font-light">
            Full-Stack Developer & IT Student
          </p>

          {/* Location */}
          <div className="animate-fade-up-delay-3 flex items-center justify-center gap-2 text-primary-foreground/70 mb-10">
            <MapPin size={18} className="text-accent" />
            <span className="text-sm md:text-base">Coimbatore, Tamil Nadu</span>
          </div>

          {/* Social Links */}
          <div className="animate-fade-up-delay-3 flex items-center justify-center gap-4 mb-12">
            <a
              href="mailto:alagarashwin.k@gmail.com"
              className="p-3 rounded-full bg-primary-foreground/10 hover:bg-accent hover:text-accent-foreground transition-all duration-300 hover:scale-110"
              aria-label="Email"
            >
              <Mail size={20} />
            </a>
            <a
              href="tel:+919894989502"
              className="p-3 rounded-full bg-primary-foreground/10 hover:bg-accent hover:text-accent-foreground transition-all duration-300 hover:scale-110"
              aria-label="Phone"
            >
              <Phone size={20} />
            </a>
            <a
              href="https://linkedin.com"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 rounded-full bg-primary-foreground/10 hover:bg-accent hover:text-accent-foreground transition-all duration-300 hover:scale-110"
              aria-label="LinkedIn"
            >
              <Linkedin size={20} />
            </a>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 rounded-full bg-primary-foreground/10 hover:bg-accent hover:text-accent-foreground transition-all duration-300 hover:scale-110"
              aria-label="GitHub"
            >
              <Github size={20} />
            </a>
          </div>

          {/* CTA Button */}
          <button
            onClick={handleScrollToAbout}
            className="animate-fade-up-delay-3 group inline-flex items-center gap-2 px-6 py-3 bg-accent text-accent-foreground rounded-full font-medium hover:bg-accent-hover transition-all duration-300 hover:scale-105"
          >
            Learn More
            <ArrowDown size={18} className="group-hover:translate-y-1 transition-transform" />
          </button>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 rounded-full border-2 border-primary-foreground/30 flex justify-center pt-2">
          <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
        </div>
      </div>
    </section>
  );
};

export default Hero;
