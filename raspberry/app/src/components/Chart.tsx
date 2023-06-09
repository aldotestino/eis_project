import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { formatDate } from '../utils';
import { Heading, VStack } from '@chakra-ui/react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface ChartProps {
  title: string
  timestamps: string[]
  values: number[]
}

function Chart({ title, timestamps, values }: ChartProps) {

  return (
    <VStack w="full" spacing={2}>
      <Heading size="lg">{title}</Heading>
      <Line options={{
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
          title: {
            display: false
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#CBD5E0'
            }
          },
          y: {
            ticks: {
              color: '#CBD5E0'
            }
          }
        }
      }} 
      data={{
        labels: timestamps.map(t => formatDate(t).substring(10)),
        datasets: [
          {
            data: values,
            borderColor: '#D6BCFA',
            backgroundColor: '#B794F4',
          }
        ]
      }} />
    </VStack>
  );
}

export default Chart;