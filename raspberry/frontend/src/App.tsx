import { Heading, VStack, Spinner, HStack, Text, SimpleGrid, Stack } from '@chakra-ui/react';
import { useQuery } from 'react-query';
import { getHome } from './services/station';
import { formatDate } from './utils';
import Card from './components/Card';
import Chart from './components/Chart';

interface ApiResponse {
  timestamps: string[]
  temperatures: number[]
  humidities: number[]
  pressures: number[]
  prediction: number
}

function App() {

  const { data, isLoading } = useQuery<ApiResponse>(['home'], () => getHome(), {
    refetchOnWindowFocus: false
  });

  console.log(data);

  return (
    <VStack spacing={10} minH="100vh" py={10}>
      <Heading px={10} textAlign="center" size="2xl">Stazione Meteo</Heading>
      {(isLoading || !data) ? 
        <Spinner color="purple.200" size="lg" /> :
        <>
          <Stack direction={['column', 'row']} align="center" spacing={[2, 2, 10]} px={10}>
            <Text fontSize="xl" fontWeight="bold">Ultimo aggiornamento:</Text>
            <Text fontSize="xl" color="gray.300">{formatDate(data.timestamps[data.timestamps.length - 1])}</Text>
          </Stack>
          <HStack spacing={10} px={10} w="full" maxW="container.xl" justify="space-between" overflowX="scroll">
            <Card property="Temperatura" value={data.temperatures[data.temperatures.length - 1]} unit="°C" />
            <Card property="Umidità" value={data.humidities[data.humidities.length - 1]} unit="%" />
            <Card property="Pressione" value={data.pressures[data.pressures.length - 1]} unit="hPA" />
          </HStack>
          <VStack spacing={2} px={[2, 2, 10]}>
            <Text textAlign="center" fontSize="xl" fontWeight="bold">Probabilità di pioggia nella prossima ora:</Text>
            <HStack align="baseline" spacing={1}>
              <Heading color="purple.300" size="3xl">{Math.round(data.prediction * 100)}</Heading>
              <Text fontSize="3xl" color="gray.300">%</Text>
            </HStack>
          </VStack>
          <SimpleGrid px={[2, 2, 10]} w="full" columns={[1, 1, 1, 2, 3]} spacing={4}>
            <Chart title="Temperatura" timestamps={data.timestamps} values={data.temperatures} />
            <Chart title="Umidità" timestamps={data.timestamps} values={data.humidities} />
            <Chart title="Pressione" timestamps={data.timestamps} values={data.pressures} />
          </SimpleGrid>
        </>
      }
    </VStack>
  );
}

export default App;
