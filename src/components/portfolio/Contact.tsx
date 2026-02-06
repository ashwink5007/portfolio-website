import { Mail, Phone, MapPin, Linkedin, Github, Send } from "lucide-react";

const Contact = () => {
  return (
    <section id="contact" className="py-20 md:py-28 bg-hero-gradient text-primary-foreground relative">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-accent/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-6 relative z-10">
        <div className="max-w-4xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Get In <span className="text-accent">Touch</span>
            </h2>
            <div className="w-20 h-1 bg-accent mx-auto rounded-full mb-6" />
            <p className="text-primary-foreground/80 text-lg max-w-xl mx-auto">
              I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
            </p>
          </div>

          {/* Contact Cards */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
            <a
              href="mailto:alagarashwin.k@gmail.com"
              className="group flex flex-col items-center p-6 bg-primary-foreground/5 backdrop-blur rounded-xl border border-primary-foreground/10 hover:bg-primary-foreground/10 hover:border-accent/50 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-full bg-accent/20 flex items-center justify-center mb-3 group-hover:bg-accent/30 transition-colors">
                <Mail className="text-accent" size={20} />
              </div>
              <span className="text-xs text-primary-foreground/60 mb-1">Email</span>
              <span className="text-sm font-medium text-center break-all">alagarashwin.k@gmail.com</span>
            </a>

            <a
              href="tel:+919894989502"
              className="group flex flex-col items-center p-6 bg-primary-foreground/5 backdrop-blur rounded-xl border border-primary-foreground/10 hover:bg-primary-foreground/10 hover:border-accent/50 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-full bg-accent/20 flex items-center justify-center mb-3 group-hover:bg-accent/30 transition-colors">
                <Phone className="text-accent" size={20} />
              </div>
              <span className="text-xs text-primary-foreground/60 mb-1">Phone</span>
              <span className="text-sm font-medium">+91 98949 89502</span>
            </a>

            <a
              href="https://www.linkedin.com/in/alagar-ashwin-k-625444283"
              target="_blank"
              rel="noopener noreferrer"
              className="group flex flex-col items-center p-6 bg-primary-foreground/5 backdrop-blur rounded-xl border border-primary-foreground/10 hover:bg-primary-foreground/10 hover:border-accent/50 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-full bg-accent/20 flex items-center justify-center mb-3 group-hover:bg-accent/30 transition-colors">
                <Linkedin className="text-accent" size={20} />
              </div>
              <span className="text-xs text-primary-foreground/60 mb-1">LinkedIn</span>
              <span className="text-sm font-medium">Connect with me</span>
            </a>

            <a
              href="https://github.com/ashwink5007"
              target="_blank"
              rel="noopener noreferrer"
              className="group flex flex-col items-center p-6 bg-primary-foreground/5 backdrop-blur rounded-xl border border-primary-foreground/10 hover:bg-primary-foreground/10 hover:border-accent/50 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-full bg-accent/20 flex items-center justify-center mb-3 group-hover:bg-accent/30 transition-colors">
                <Github className="text-accent" size={20} />
              </div>
              <span className="text-xs text-primary-foreground/60 mb-1">GitHub</span>
              <span className="text-sm font-medium">View my code</span>
            </a>
          </div>

          {/* Location */}
          <div className="flex items-center justify-center gap-2 text-primary-foreground/70 mb-12">
            <MapPin size={18} className="text-accent" />
            <span>Coimbatore, Tamil Nadu, India</span>
          </div>

          {/* CTA */}
          <div className="text-center">
            <a
              href="mailto:alagarashwin.k@gmail.com"
              className="inline-flex items-center gap-2 px-8 py-4 bg-accent text-accent-foreground rounded-full font-medium hover:bg-accent-hover transition-all duration-300 hover:scale-105 text-lg"
            >
              <Send size={20} />
              Send Me a Message
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
