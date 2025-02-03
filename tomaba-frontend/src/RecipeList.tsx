import { List, Spinner, Text, VStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function RecipeList() {
  const [recipeIds, setRecipeIds] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/recipes`)
      .then((res) => res.json())
      .then((data) => {
        setRecipeIds(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <Spinner size="xl" />;
  if (error) return <Text color="red.500">{error}</Text>;
  if (recipeIds.length === 0) return <Text>No recipes found.</Text>;

  return (
    <VStack gap={4} align="start">
      <Text fontSize="xl" fontWeight="bold">
        Available Recipes
      </Text>
      <List.Root gap={2}>
        {recipeIds.map((id) => (
          <List.Item key={id}>
            <RouterLink to={`/recipe/${id}`} style={{ color: "blue" }}>
              Recipe {id}
            </RouterLink>
          </List.Item>
        ))}
      </List.Root>
    </VStack>
  );
}

export default RecipeList;
