import { Box, Heading, IconButton } from "@chakra-ui/react";
import { FaHome } from "react-icons/fa"; // Import Home icon

import { Link, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import RecipeList from "./RecipeList.tsx";
import RecipePage from "./RecipePage.tsx";

function App() {
  return (
    <Router>
      <Box maxW="800px" mx="auto" p={4}>
        {/* Home Icon */}
        <Link to="/">
          <IconButton
            aria-label="Home"
            size="lg"
            variant="ghost"
            color="blue.500"
            _hover={{ bg: "gray.200" }}
          >
            <FaHome />
          </IconButton>
        </Link>

        <Heading as="h1" size="xl" mb={4} textAlign="center">
          Tomaba
        </Heading>

        <Routes>
          <Route path="/" element={<RecipeList />} />
          <Route path="/recipe/:id" element={<RecipePage />} />
        </Routes>
      </Box>
    </Router>
  );
}

export default App;
