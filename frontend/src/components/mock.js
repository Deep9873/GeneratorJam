// Mock data for Generator Jam
export const mockGeneratedContent = {
  text: {
    blog: {
      title: "The Future of AI-Powered Content Creation",
      content: `# The Future of AI-Powered Content Creation

The digital landscape is evolving at breakneck speed, and artificial intelligence is leading the charge in revolutionizing how we create, consume, and interact with content. From automated blog posts to AI-generated images, we're witnessing a paradigm shift that's reshaping entire industries.

## The Current State of AI Content Generation

Today's AI tools can produce human-like text, stunning visuals, and even video content with remarkable accuracy. These systems have learned from vast datasets, enabling them to understand context, tone, and style in ways that were unimaginable just a few years ago.

## Key Benefits for Content Creators

- **Speed**: Generate content in minutes instead of hours
- **Consistency**: Maintain brand voice across all platforms
- **Scalability**: Produce large volumes of content efficiently
- **Creativity**: Spark new ideas and overcome writer's block

## The Road Ahead

As AI technology continues to advance, we can expect even more sophisticated tools that blur the line between human and machine creativity. The future belongs to those who can effectively harness these powerful capabilities while maintaining the human touch that makes content truly engaging.

*Generated with love by Generator Jam*`,
      wordCount: 187,
      readingTime: "1 min read"
    },
    twitter: {
      content: "🚀 Just discovered Generator Jam - the AI-powered content creation tool that's changing the game! \n\n✨ Generate blog posts, social media content, and images instantly\n💡 Perfect for creators, marketers, and businesses\n\n#AI #ContentCreation #Innovation #TechTool",
      characterCount: 278,
      hashtags: ["#AI", "#ContentCreation", "#Innovation", "#TechTool"]
    },
    instagram: {
      content: "Transform your content strategy with AI! 🎨✨\n\nCreating engaging posts has never been easier. Whether you're a small business owner, influencer, or content creator, AI tools like Generator Jam are revolutionizing how we connect with our audience.\n\nKey benefits:\n• Save hours of brainstorming\n• Maintain consistent brand voice\n• Generate ideas on demand\n• Scale your content production\n\nWhat's your experience with AI content tools? Drop a comment below! 👇\n\n#ContentCreation #AITools #SocialMediaMarketing #CreativeProcess #Innovation #TechTrends",
      characterCount: 543,
      hashtags: ["#ContentCreation", "#AITools", "#SocialMediaMarketing", "#CreativeProcess", "#Innovation", "#TechTrends"]
    },
    linkedin: {
      content: "The content creation landscape is undergoing a seismic shift, and AI is at the epicenter of this transformation.\n\nAs a professional who's spent years crafting content strategies, I've witnessed firsthand how AI tools are democratizing content creation. What once required entire teams can now be accomplished by individuals with the right tools and mindset.\n\nKey insights from my experience:\n\n1. AI doesn't replace creativity - it amplifies it\n2. The human touch remains irreplaceable for strategy and emotional connection\n3. Efficiency gains are real, but quality control is crucial\n4. The future belongs to those who can blend human insight with AI capabilities\n\nTools like Generator Jam are making sophisticated content creation accessible to everyone, from solopreneurs to Fortune 500 companies.\n\nWhat's your take on AI in content creation? Are you embracing these tools or still on the fence?\n\n#ContentStrategy #ArtificialIntelligence #DigitalMarketing #Innovation #FutureOfWork",
      characterCount: 1089,
      hashtags: ["#ContentStrategy", "#ArtificialIntelligence", "#DigitalMarketing", "#Innovation", "#FutureOfWork"]
    }
  },
  images: [
    {
      url: "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBmaWxsPSJsaW5lYXItZ3JhZGllbnQoNDVkZWcsICM2MzY2RjEsICM4QjVDRjYpIi8+Cjx0ZXh0IHg9IjI1NiIgeT0iMjgwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4cHgiIGZvbnQtd2VpZ2h0PSJib2xkIj5BSSBHZW5lcmF0ZWQgSW1hZ2U8L3RleHQ+CjwvdGV4dD4KPC9zdmc+",
      prompt: "A futuristic AI brain with digital neural networks",
      dimensions: "512x512",
      format: "PNG"
    },
    {
      url: "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBmaWxsPSJsaW5lYXItZ3JhZGllbnQoNDVkZWcsICNGRjc5MzIsICNGRkIzNzMpIi8+Cjx0ZXh0IHg9IjI1NiIgeT0iMjgwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4cHgiIGZvbnQtd2VpZ2h0PSJib2xkIj5Db250ZW50IENyZWF0aW9uPC90ZXh0Pgo8L3N2Zz4=",
      prompt: "Creative workspace with digital tools and content elements",
      dimensions: "512x512",
      format: "PNG"
    }
  ]
};

export const mockHistory = [
  {
    id: "1",
    type: "text",
    contentType: "blog",
    prompt: "Write a blog post about the future of AI in content creation",
    result: mockGeneratedContent.text.blog,
    timestamp: new Date(Date.now() - 86400000).toISOString(),
    isFavorite: true
  },
  {
    id: "2",
    type: "image",
    contentType: "general",
    prompt: "A futuristic AI brain with digital neural networks",
    result: mockGeneratedContent.images[0],
    timestamp: new Date(Date.now() - 172800000).toISOString(),
    isFavorite: false
  },
  {
    id: "3",
    type: "text",
    contentType: "twitter",
    prompt: "Create a Twitter thread about AI content generation benefits",
    result: mockGeneratedContent.text.twitter,
    timestamp: new Date(Date.now() - 259200000).toISOString(),
    isFavorite: true
  },
  {
    id: "4",
    type: "text",
    contentType: "instagram",
    prompt: "Instagram post about AI tools for content creators",
    result: mockGeneratedContent.text.instagram,
    timestamp: new Date(Date.now() - 345600000).toISOString(),
    isFavorite: false
  },
  {
    id: "5",
    type: "text",
    contentType: "linkedin",
    prompt: "Professional LinkedIn post about AI in content strategy",
    result: mockGeneratedContent.text.linkedin,
    timestamp: new Date(Date.now() - 432000000).toISOString(),
    isFavorite: true
  }
];

export const contentTemplates = {
  blog: {
    name: "Blog Post",
    icon: "📝",
    placeholder: "Write a blog post about sustainable technology trends in 2024",
    description: "Generate comprehensive blog posts with engaging titles and structured content"
  },
  twitter: {
    name: "Twitter Post",
    icon: "🐦",
    placeholder: "Create a Twitter thread about productivity tips for remote workers",
    description: "Craft engaging tweets with optimal character count and hashtags"
  },
  instagram: {
    name: "Instagram Caption",
    icon: "📸",
    placeholder: "Write an Instagram caption for a coffee shop's morning special",
    description: "Create captivating Instagram posts with emojis and relevant hashtags"
  },
  linkedin: {
    name: "LinkedIn Article",
    icon: "💼",
    placeholder: "Write a professional LinkedIn post about leadership in the digital age",
    description: "Generate professional content for thought leadership and networking"
  },
  image: {
    name: "AI Image",
    icon: "🎨",
    placeholder: "A serene mountain landscape at sunset with purple and orange sky",
    description: "Generate stunning AI images from detailed text descriptions"
  }
};

// Mock loading messages
export const loadingMessages = [
  "Igniting creative sparks...",
  "Brewing the perfect content...",
  "Assembling words with precision...",
  "Painting with pixels...",
  "Crafting your masterpiece...",
  "Almost there, adding final touches...",
  "Polishing the magic..."
];

export const getRandomLoadingMessage = () => {
  return loadingMessages[Math.floor(Math.random() * loadingMessages.length)];
};