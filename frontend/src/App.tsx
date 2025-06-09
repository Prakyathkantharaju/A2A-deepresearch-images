import React, { useState } from 'react';
import {
  Box,
  Container,
  VStack,
  HStack,
  Text,
  Textarea,
  Button,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Divider,
  Badge,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Progress,
  Spinner,
  useToast,
  Flex,
  Icon,
} from '@chakra-ui/react';
import { SearchIcon, RepeatIcon } from '@chakra-ui/icons';

interface PipelineResult {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  result?: any;
  error?: string;
}

function App() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<PipelineResult[]>([]);
  const toast = useToast();

  const handleSubmit = async () => {
    if (!prompt.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter a prompt',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    
    // Create a new pipeline result
    const newResult: PipelineResult = {
      id: Date.now().toString(),
      status: 'pending'
    };
    
    setResults(prev => [newResult, ...prev]);

    try {
      // TODO: Replace this with actual API call to your backend
      // This is just a placeholder simulation
      setTimeout(() => {
        setResults(prev => 
          prev.map(r => 
            r.id === newResult.id 
              ? { ...r, status: 'running' as const }
              : r
          )
        );
      }, 500);

      setTimeout(() => {
        setResults(prev => 
          prev.map(r => 
            r.id === newResult.id 
              ? { 
                  ...r, 
                  status: 'completed' as const,
                  result: `Deep research completed for: "${prompt}"`
                }
              : r
          )
        );
        setIsLoading(false);
        setPrompt('');
        toast({
          title: 'Success',
          description: 'Deep research pipeline completed!',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      }, 3000);

    } catch (error) {
      setResults(prev => 
        prev.map(r => 
          r.id === newResult.id 
            ? { 
                ...r, 
                status: 'error' as const,
                error: 'Failed to process request'
              }
            : r
        )
      );
      setIsLoading(false);
      toast({
        title: 'Error',
        description: 'Failed to start pipeline',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const getStatusColor = (status: PipelineResult['status']) => {
    switch (status) {
      case 'pending': return 'yellow';
      case 'running': return 'blue';
      case 'completed': return 'green';
      case 'error': return 'red';
      default: return 'gray';
    }
  };

  return (
    <Box minH="100vh" bg="gray.50">
      <Container maxW="4xl" py={8}>
        <VStack spacing={8} align="stretch">
          {/* Header */}
          <Box textAlign="center">
            <HStack justify="center" mb={2}>
              <Icon as={SearchIcon} w={8} h={8} color="blue.500" />
              <Heading as="h1" size="2xl" color="gray.800">
                DeepResearch Pipeline
              </Heading>
            </HStack>
            <Text fontSize="lg" color="gray.600">
              Advanced AI-powered research and analysis platform
            </Text>
          </Box>

          {/* Input Section */}
          <Card>
            <CardHeader>
              <Heading size="md">Research Query</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4}>
                <Textarea
                  placeholder="Enter your research prompt here... (e.g., 'Analyze the latest trends in renewable energy technologies')"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  rows={4}
                  resize="vertical"
                  focusBorderColor="blue.500"
                />
                <Flex justify="space-between" w="full" align="center">
                  <Text fontSize="sm" color="gray.500">
                    {prompt.length} characters
                  </Text>
                  <Button
                    colorScheme="blue"
                    onClick={handleSubmit}
                    isLoading={isLoading}
                    loadingText="Processing..."
                    leftIcon={<SearchIcon />}
                    size="lg"
                    disabled={!prompt.trim()}
                  >
                    Start Research
                  </Button>
                </Flex>
              </VStack>
            </CardBody>
          </Card>

          {/* Results Section */}
          {results.length > 0 && (
            <Card>
              <CardHeader>
                <HStack justify="space-between">
                  <Heading size="md">Research Results</Heading>
                  <Badge colorScheme="blue" variant="subtle">
                    {results.length} {results.length === 1 ? 'query' : 'queries'}
                  </Badge>
                </HStack>
              </CardHeader>
              <CardBody>
                <VStack spacing={4} align="stretch">
                  {results.map((result) => (
                    <Card key={result.id} variant="outline">
                      <CardBody>
                        <VStack align="stretch" spacing={3}>
                          <HStack justify="space-between">
                            <Badge 
                              colorScheme={getStatusColor(result.status)}
                              variant="solid"
                            >
                              {result.status.toUpperCase()}
                            </Badge>
                            <Text fontSize="sm" color="gray.500">
                              ID: {result.id}
                            </Text>
                          </HStack>

                          {result.status === 'running' && (
                            <Box>
                              <HStack mb={2}>
                                <Spinner size="sm" color="blue.500" />
                                <Text fontSize="sm" color="blue.600">
                                  Processing your research query...
                                </Text>
                              </HStack>
                              <Progress 
                                size="sm" 
                                isIndeterminate 
                                colorScheme="blue" 
                                borderRadius="md"
                              />
                            </Box>
                          )}

                          {result.status === 'completed' && result.result && (
                            <Alert status="success" borderRadius="md">
                              <AlertIcon />
                              <Box>
                                <AlertTitle>Research Completed!</AlertTitle>
                                <AlertDescription>
                                  {result.result}
                                </AlertDescription>
                              </Box>
                            </Alert>
                          )}

                          {result.status === 'error' && result.error && (
                            <Alert status="error" borderRadius="md">
                              <AlertIcon />
                              <Box>
                                <AlertTitle>Error</AlertTitle>
                                <AlertDescription>
                                  {result.error}
                                </AlertDescription>
                              </Box>
                            </Alert>
                          )}

                          {result.status === 'pending' && (
                            <Alert status="info" borderRadius="md">
                              <AlertIcon />
                              <AlertDescription>
                                Your research query has been queued and will start processing shortly...
                              </AlertDescription>
                            </Alert>
                          )}
                        </VStack>
                      </CardBody>
                    </Card>
                  ))}
                </VStack>
              </CardBody>
            </Card>
          )}

          {/* Empty State */}
          {results.length === 0 && (
            <Card variant="outline" borderStyle="dashed">
              <CardBody textAlign="center" py={12}>
                <VStack spacing={4}>
                  <Icon as={RepeatIcon} w={12} h={12} color="gray.400" />
                  <Box>
                    <Text fontSize="lg" fontWeight="medium" color="gray.600">
                      Ready to start your research
                    </Text>
                    <Text color="gray.500">
                      Enter a prompt above to begin deep research analysis
                    </Text>
                  </Box>
                </VStack>
              </CardBody>
            </Card>
          )}
        </VStack>
      </Container>
    </Box>
  );
}

export default App;
