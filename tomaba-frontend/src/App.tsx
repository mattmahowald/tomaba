import { Box, Heading, SimpleGrid, Spinner, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";

const RECIPE_API_URL = "http://127.0.0.1:8000/recipe/1";

interface Ingredient {
  quantity: string;
  unit: string;
}

interface Recipe {
  name: string;
  summary: string;
  cuisine: string;
  difficulty: string;
  prep_time: number;
  cook_time: number;
  servings: number;
  ingredients: Record<string, Ingredient>;
  steps: string[];
}

function App() {
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(RECIPE_API_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch recipe");
        }
        return response.json();
      })
      .then((data: Recipe) => {
        setRecipe(data);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <Spinner size="xl" />;
  if (error) return <Text color="red.500">{error}</Text>;
  if (!recipe) return null;

  return (
    <Box maxW="800px" mx="auto" p={4}>
      <Heading as="h1" size="xl" mb={4}>
        {recipe.name}
      </Heading>
      <SimpleGrid columns={2} gap={10}>
        <Box>
          <Heading as="h2" size="lg" mb={2}>
            Ingredients
          </Heading>
          {Object.entries(recipe.ingredients).map(([name, details]) => (
            <Text key={name}>
              {name}: {details.quantity} {details.unit}
            </Text>
          ))}
        </Box>
        <Box>
          <Heading as="h2" size="lg" mb={2}>
            Steps
          </Heading>
          {recipe.steps.map((step, index) => (
            <Text key={index}>
              {index + 1}. {step}
            </Text>
          ))}
        </Box>
      </SimpleGrid>
    </Box>
  );
}

export default App;
