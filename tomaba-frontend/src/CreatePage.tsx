import {
  Box,
  Flex,
  IconButton,
  Input,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";
import { useToast } from "@chakra-ui/toast";
import { useState } from "react";
import { FaPaperPlane } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function CreatePage() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const handleSend = async () => {
    if (!input.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/recipe/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: input }),
      });

      const data = await response.json();
      if (response.ok && data.recipe_id) {
        navigate(`/recipe/${data.recipe_id}`);
      } else {
        toast({
          title: "Error",
          description: "Failed to generate a recipe.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      toast({
        title: "Network Error",
        description: "Could not connect to the server.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      maxW="800px"
      mx="auto"
      p={6}
      bg="white"
      boxShadow="lg"
      borderRadius="lg"
      minH="500px"
      display="flex"
      flexDirection="column"
      justifyContent="space-between"
    >
      <VStack gap={4} align="stretch" flex="1">
        <Text fontSize="xl" fontWeight="bold" textAlign="center">
          Create a New Recipe
        </Text>

        {/* Chat Input Box */}
        <Flex gap={2} mt="auto">
          <Input
            placeholder="Describe your recipe idea..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            size="lg"
            borderRadius="full"
          />
          <IconButton
            aria-label="Send"
            colorScheme="blue"
            disabled={loading || !input.trim()}
            onClick={handleSend}
            size="lg"
            borderRadius="full"
          >
            {loading ? <Spinner size="sm" /> : <FaPaperPlane />}
          </IconButton>
        </Flex>
      </VStack>
    </Box>
  );
}

export default CreatePage;
