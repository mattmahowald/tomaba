import { Box, Heading, SimpleGrid, Spinner, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

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

function RecipePage() {
  const { id } = useParams<{ id: string }>();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/recipe/${id}`)
      .then((res) => res.json())
      .then((data: Recipe) => {
        setRecipe(data);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <Spinner size="xl" />;
  if (error) return <Text color="red.500">{error}</Text>;
  if (!recipe) return null;

  return (
    <Box>
      <Heading as="h2" size="xl" mb={4}>
        {recipe.name}
      </Heading>
      <Text fontSize="lg" fontStyle="italic">
        {recipe.summary}
      </Text>
      <SimpleGrid columns={2} gap={10} mt={4}>
        <Box>
          <Heading as="h3" size="md">
            Ingredients
          </Heading>
          {Object.entries(recipe.ingredients).map(([name, details]) => (
            <Text key={name}>
              {name}: {details.quantity} {details.unit}
            </Text>
          ))}
        </Box>
        <Box>
          <Heading as="h3" size="md">
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

export default RecipePage;
