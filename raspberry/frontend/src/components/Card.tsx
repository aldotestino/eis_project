import { Heading, VStack, Text, HStack } from '@chakra-ui/react';

interface CardProps {
  property: string
  value: number
  unit: string
}

function Card({ property, value, unit }: CardProps) {
  return (
    <VStack bg="gray.700" minW="360px" py={7} align="start" pl={7} borderRadius="xl" boxShadow="md" >
      <Heading size="xl">{property}</Heading>
      <HStack align="baseline" spacing={1}>
        <Heading color="purple.300" size="3xl">{Math.round(value)}</Heading>
        <Text fontSize="3xl" color="gray.300">{unit}</Text>
      </HStack>
    </VStack>
  );
}

export default Card;