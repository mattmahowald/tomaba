import {
  Grid,
  Heading,
  LinkBox,
  LinkOverlay,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";
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

  if (loading) return <Spinner size="xl" mt={10} />;
  if (error)
    return (
      <Text color="red.500" mt={4}>
        {error}
      </Text>
    );
  if (recipeIds.length === 0) return <Text mt={4}>No recipes found.</Text>;

  return (
    <VStack gap={6} align="start" w="100%">
      <Heading as="h2" size="xl" fontWeight="bold">
        Discover Recipes
      </Heading>

      {/* Grid Layout for Recipe Cards */}
      <Grid
        templateColumns={{ base: "1fr", md: "repeat(2, 1fr)" }}
        gap={6}
        w="100%"
      >
        {recipeIds.map((id) => (
          <LinkBox
            key={id}
            as="article"
            p={5}
            borderRadius="lg"
            boxShadow="md"
            bg="white"
            transition="transform 0.2s ease-in-out"
            _hover={{ transform: "scale(1.03)", boxShadow: "lg" }}
          >
            {/* Correctly using `RouterLink` inside `LinkOverlay` */}
            <Heading as="h3" size="md" mb={2}>
              <LinkOverlay>
                <RouterLink to={`/recipe/${id}`}>Recipe {id}</RouterLink>
              </LinkOverlay>
            </Heading>
            <Text fontSize="sm" color="gray.600">
              Click to view details
            </Text>
          </LinkBox>
        ))}
      </Grid>
    </VStack>
  );
}

export default RecipeList;
